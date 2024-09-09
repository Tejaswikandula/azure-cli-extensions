# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from azure.cli.core import AzCommandsLoader
from azure.cli.core.profiles import register_resource_type
from azure.cli.core.commands import AzCommandGroup, AzArgumentContext
from .profiles import CUSTOM_DATA_STORAGE_BLOB

from ._help import helps  # pylint: disable=unused-import


class StorageCommandsLoader(AzCommandsLoader):
    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        register_resource_type('latest', CUSTOM_DATA_STORAGE_BLOB, '2021-12-02')
        storage_custom = CliCommandType(operations_tmpl='azure.cli.command_modules.storage.custom#{}')
        super(StorageCommandsLoader, self).__init__(cli_ctx=cli_ctx,
                                                    resource_type=CUSTOM_DATA_STORAGE_BLOB,
                                                    custom_command_type=storage_custom,
                                                    command_group_cls=StorageCommandGroup,
                                                    argument_context_cls=StorageArgumentContext)

    def load_command_table(self, args):
        from .commands import load_command_table
        load_command_table(self, args)
        return self.command_table

    def load_arguments(self, command):
        from ._params import load_arguments
        load_arguments(self, command)


class StorageArgumentContext(AzArgumentContext):
    def register_sas_arguments(self):
        from ._validators import ipv4_range_type, get_datetime_type
        self.argument('ip', type=ipv4_range_type,
                      help='Specifies the IP address or range of IP addresses from which to accept requests. Supports '
                           'only IPv4 style addresses.')
        self.argument('expiry', type=get_datetime_type(True),
                      help='Specifies the UTC datetime (Y-m-d\'T\'H:M\'Z\') at which the SAS becomes invalid. Do not '
                           'use if a stored access policy is referenced with --id that specifies this value.')
        self.argument('start', type=get_datetime_type(True),
                      help='Specifies the UTC datetime (Y-m-d\'T\'H:M\'Z\') at which the SAS becomes valid. Do not use '
                           'if a stored access policy is referenced with --id that specifies this value. Defaults to '
                           'the time of the request.')
        self.argument('protocol', options_list=('--https-only',), action='store_const', const='https',
                      help='Only permit requests made with the HTTPS protocol. If omitted, requests from both the HTTP '
                           'and HTTPS protocol are permitted.')

    def register_content_settings_argument(self, settings_class, update, arg_group=None, guess_from_file=None):
        from ._validators import get_content_setting_validator
        from azure.cli.core.commands.parameters import get_three_state_flag

        self.ignore('content_settings')
        self.extra('content_type', default=None, help='The content MIME type.', arg_group=arg_group,
                   validator=get_content_setting_validator(settings_class, update, guess_from_file=guess_from_file,
                                                           process_md5=True))
        self.extra('content_encoding', default=None, help='The content encoding type.', arg_group=arg_group)
        self.extra('content_language', default=None, help='The content language.', arg_group=arg_group)
        self.extra('content_disposition', default=None, arg_group=arg_group,
                   help='Conveys additional information about how to process the response payload, and can also be '
                        'used to attach additional metadata.')
        self.extra('content_cache_control', options_list=['--content-cache-control', '--content-cache'],
                   default=None, help='The cache control string.',
                   arg_group=arg_group)
        self.extra('content_md5', default=None, help='The content\'s MD5 hash.', arg_group=arg_group)
        if update:
            self.extra('clear_content_settings', help='If this flag is set, then if any one or more of the '
                       'following properties (--content-cache-control, --content-disposition, --content-encoding, '
                       '--content-language, --content-md5, --content-type) is set, then all of these properties are '
                       'set together. If a value is not provided for a given property when at least one of the '
                       'properties listed below is set, then that property will be cleared.',
                       arg_type=get_three_state_flag())

    def register_path_argument(self, default_file_param=None, options_list=None):
        from ._validators import get_file_path_validator
        from .completers import file_path_completer

        path_help = 'The path to the file within the file share.'
        if default_file_param:
            path_help = '{} If the file name is omitted, the source file name will be used.'.format(path_help)
        self.extra('path', options_list=options_list or ('--path', '-p'),
                   required=default_file_param is None, help=path_help,
                   validator=get_file_path_validator(default_file_param=default_file_param),
                   completer=file_path_completer)
        self.ignore('file_name')
        self.ignore('directory_name')

    def register_source_uri_arguments(self, validator, blob_only=False):
        self.argument('source_url', options_list=('--source-uri', '-u'), validator=validator, required=False,
                      arg_group='Copy Source')
        self.extra('source_sas', default=None, arg_group='Copy Source',
                   help='The shared access signature for the source storage account.')
        self.extra('source_container', default=None, arg_group='Copy Source',
                   help='The container name for the source storage account.')
        self.extra('source_blob', default=None, arg_group='Copy Source',
                   help='The blob name for the source storage account.')
        self.extra('source_snapshot', default=None, arg_group='Copy Source',
                   help='The blob snapshot for the source storage account.')
        self.extra('source_account_name', default=None, arg_group='Copy Source',
                   help='The storage account name of the source blob.')
        self.extra('source_account_key', default=None, arg_group='Copy Source',
                   help='The storage account key of the source blob.')
        if not blob_only:
            self.extra('source_path', default=None, arg_group='Copy Source',
                       help='The file path for the source storage account.')
            self.extra('source_share', default=None, arg_group='Copy Source',
                       help='The share name for the source storage account.')

    def register_precondition_options(self, prefix=''):
        from ._validators import (get_datetime_type)
        self.extra('{}if_modified_since'.format(prefix), arg_group='Precondition',
                   help="Commence only if modified since supplied UTC datetime (Y-m-d'T'H:M'Z').",
                   type=get_datetime_type(False))
        self.extra('{}if_unmodified_since'.format(prefix), arg_group='Precondition',
                   help="Commence only if unmodified since supplied UTC datetime (Y-m-d'T'H:M'Z').",
                   type=get_datetime_type(False))
        self.extra('{}if_match'.format(prefix), arg_group='Precondition',
                   help="An ETag value, or the wildcard character (*). Specify this header to perform the "
                        "operation only if the resource's ETag matches the value specified.")
        self.extra('{}if_none_match'.format(prefix), arg_group='Precondition',
                   help="An ETag value, or the wildcard character (*). Specify this header to perform "
                        "the operation only if the resource's ETag does not match the value specified. Specify the wildcard "
                        "character (*) to perform the operation only if the resource does not exist, and fail the operation "
                        "if it does exist.")
        self.extra('{}if_tags_match_condition'.format(prefix), arg_group='Precondition',
                   options_list=['--{}tags-condition'.format(prefix.replace('_', '-'))],
                   help='Specify a SQL where clause on blob tags to operate only on blobs with a matching value.')

    def register_blob_arguments(self):
        from ._validators import validate_blob_arguments
        self.extra('blob_name')
        self.extra('container_name')
        self.extra('timeout', help='Request timeout in seconds. Applies to each call to the service.', type=int)
        self.extra('blob_url', help='The full endpoint URL to the Blob, including SAS token and snapshot if used. '
                   'This could be either the primary endpoint, or the secondary endpoint depending on the current '
                   '`location_mode`.', validator=validate_blob_arguments)

    def register_lease_blob_arguments(self):
        self.extra('blob_name', required=True)
        self.extra('container_name', required=True)
        self.extra('timeout', help='Request timeout in seconds. Applies to each call to the service.', type=int)

    def register_container_arguments(self):
        self.extra('container_name', required=True)
        self.extra('timeout', help='Request timeout in seconds. Applies to each call to the service.', type=int)


class StorageCommandGroup(AzCommandGroup):
    def storage_command(self, name, method_name=None, command_type=None, oauth=False, generic_update=None, **kwargs):
        """ Registers an Azure CLI Storage Data Plane command. These commands always include the four parameters which
        can be used to obtain a storage client: account-name, account-key, connection-string, and sas-token. """
        if generic_update:
            command_name = '{} {}'.format(self.group_name, name) if self.group_name else name
            self.generic_update_command(name, **kwargs)
        elif command_type:
            command_name = self.command(name, method_name, command_type=command_type, **kwargs)
        else:
            command_name = self.command(name, method_name, **kwargs)
        self._register_data_plane_account_arguments(command_name)
        if oauth:
            self._register_data_plane_oauth_arguments(command_name)

    def storage_command_oauth(self, *args, **kwargs):
        _merge_new_exception_handler(kwargs, self.get_handler_suppress_some_400())
        self.storage_command(*args, oauth=True, **kwargs)

    def storage_custom_command(self, name, method_name, oauth=False, **kwargs):
        command_name = self.custom_command(name, method_name, **kwargs)
        self._register_data_plane_account_arguments(command_name)
        if oauth:
            self._register_data_plane_oauth_arguments(command_name)

    def storage_custom_command_oauth(self, *args, **kwargs):
        _merge_new_exception_handler(kwargs, self.get_handler_suppress_some_400())
        self.storage_custom_command(*args, oauth=True, **kwargs)

    @classmethod
    def get_handler_suppress_some_400(cls):
        def handler(ex):
            if hasattr(ex, 'status_code') and ex.status_code == 403 and hasattr(ex, 'error_code'):
                # TODO: Revisit the logic here once the service team updates their response
                if ex.error_code == 'AuthorizationPermissionMismatch':
                    message = """
You do not have the required permissions needed to perform this operation.
Depending on your operation, you may need to be assigned one of the following roles:
    "Storage Blob Data Contributor"
    "Storage Blob Data Reader"
    "Storage Queue Data Contributor"
    "Storage Queue Data Reader"

If you want to use the old authentication method and allow querying for the right account key, please use the "--auth-mode" parameter and "key" value.
                    """
                    ex.args = (message,)
                elif ex.error_code == 'AuthorizationFailure':
                    message = """
The request may be blocked by network rules of storage account. Please check network rule set using 'az storage account show -n accountname --query networkRuleSet'.
If you want to change the default action to apply when no rule matches, please use 'az storage account update'.
                    """
                    ex.args = (message,)
                elif ex.error_code == 'AuthenticationFailed':
                    message = """
Authentication failure. This may be caused by either invalid account key, connection string or sas token value provided for your storage account.
                    """
                    ex.args = (message,)
            if hasattr(ex, 'status_code') and ex.status_code == 409 and ex.error_code == 'NoPendingCopyOperation':
                pass

        return handler

    def _register_data_plane_account_arguments(self, command_name):
        """ Add parameters required to create a storage client """
        from azure.cli.core.commands.parameters import get_resource_name_completion_list
        from ._validators import validate_client_parameters
        command = self.command_loader.command_table.get(command_name, None)
        if not command:
            return

        group_name = 'Storage Account'
        command.add_argument('account_name', '--account-name', required=False, default=None,
                             arg_group=group_name,
                             completer=get_resource_name_completion_list('Microsoft.Storage/storageAccounts'),
                             help='Storage account name. Related environment variable: AZURE_STORAGE_ACCOUNT. Must be '
                                  'used in conjunction with either storage account key or a SAS token. If neither are '
                                  'present, the command will try to query the storage account key using the '
                                  'authenticated Azure account. If a large number of storage commands are executed the '
                                  'API quota may be hit')
        command.add_argument('account_url', '--blob-endpoint',
                             required=False, default=None, arg_group=group_name,
                             help='Storage data service endpoint. Must be used in conjunction with either '
                                  'storage account key or a SAS token. You can find each service primary endpoint '
                                  'with `az storage account show`. '
                                  'Environment variable: AZURE_STORAGE_SERVICE_ENDPOINT')
        command.add_argument('account_key', '--account-key', required=False, default=None,
                             arg_group=group_name,
                             help='Storage account key. Must be used in conjunction with storage account name. '
                                  'Environment variable: AZURE_STORAGE_KEY')
        command.add_argument('connection_string', '--connection-string', required=False, default=None,
                             validator=validate_client_parameters, arg_group=group_name,
                             help='Storage account connection string. Environment variable: '
                                  'AZURE_STORAGE_CONNECTION_STRING')
        command.add_argument('sas_token', '--sas-token', required=False, default=None,
                             arg_group=group_name,
                             help='A Shared Access Signature (SAS). Must be used in conjunction with storage account '
                                  'name. Environment variable: AZURE_STORAGE_SAS_TOKEN')

    def _register_data_plane_oauth_arguments(self, command_name):
        from azure.cli.core.commands.parameters import get_enum_type

        # The CLI's argument registration methods assume command table has finished loading and contain checks
        # that reflect the state of the CLI at that point in time.
        # The following code bypasses those checks, as these arguments are registered in tandem with commands.
        if command_name not in self.command_loader.command_table:
            return
        self.command_loader.cli_ctx.invocation.data['command_string'] = command_name

        with self.command_loader.argument_context(command_name, min_api='2017-11-09') as c:
            c.extra('auth_mode', arg_type=get_enum_type(['login', 'key']),
                    help='The mode in which to run the command. "login" mode will directly use your login credentials '
                         'for the authentication. The legacy "key" mode will attempt to query for '
                         'an account key if no authentication parameters for the account are provided. '
                         'Environment variable: AZURE_STORAGE_AUTH_MODE')


def _merge_new_exception_handler(kwargs, handler):
    first = kwargs.get('exception_handler')

    def new_handler(ex):
        handler(ex)
        if not first:
            raise ex
        first(ex)
    kwargs['exception_handler'] = new_handler


COMMAND_LOADER_CLS = StorageCommandsLoader
