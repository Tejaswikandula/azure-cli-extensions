# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "azure-terraform export-terraform",
    is_preview=True,
)
class ExportTerraform(AAZCommand):
    """Exports the Terraform configuration of the specified resource(s)

    :example: Export a resource group targeting to `azurerm` provider
        az azure-terraform export-terraform --export-resource-group '{resource-group-name:my-rg}'

    :example: Export a list of resources targeting to `azapi` provider
        az azure-terraform export-terraform --full-properties false --target-provider azapi --export-resource '{resource-ids:[id1,id2,id3]}'

    :example: Export all virtual networks in the current subscription, together with their child resources (e.g. subnets) targeting `azapi` provider
        az azure-terraform export-terraform --full-properties false --target-provider azapi --export-query "{query:'type =~ \\"microsoft.network/virtualnetworks\\"',recursive:true}"
    """

    _aaz_info = {
        "version": "2023-07-01-preview",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/providers/microsoft.azureterraform/exportterraform", "2023-07-01-preview"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_lro_poller(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        # define Arg Group "ExportParameter"

        _args_schema = cls._args_schema
        _args_schema.export_query = AAZObjectArg(
            options=["--export-query"],
            arg_group="ExportParameter",
            help="Export parameter for resources queried by ARG (Azure Resource Graph).",
        )
        _args_schema.export_resource = AAZObjectArg(
            options=["--export-resource"],
            arg_group="ExportParameter",
            help="Export parameter for individual resources.",
        )
        _args_schema.export_resource_group = AAZObjectArg(
            options=["--export-resource-group"],
            arg_group="ExportParameter",
            help="Export parameter for a resource group.",
        )
        _args_schema.full_properties = AAZBoolArg(
            options=["--full-properties"],
            arg_group="ExportParameter",
            help="Whether to output all non-computed properties in the generated Terraform configuration? This probably needs manual modifications to make it valid",
            default=True,
        )
        _args_schema.mask_sensitive = AAZBoolArg(
            options=["--mask-sensitive"],
            arg_group="ExportParameter",
            help="Mask sensitive attributes in the Terraform configuration",
            default=True,
        )
        _args_schema.target_provider = AAZStrArg(
            options=["--target-provider"],
            arg_group="ExportParameter",
            help="The target Azure Terraform Provider",
            default="azurerm",
            enum={"azapi": "azapi", "azurerm": "azurerm"},
        )

        export_query = cls._args_schema.export_query
        export_query.name_pattern = AAZStrArg(
            options=["name-pattern"],
            help="The name pattern of the Terraform resources",
            default="res-",
        )
        export_query.query = AAZStrArg(
            options=["query"],
            help="The ARG where predicate. Note that you can combine multiple conditions in one `where` predicate, e.g. `resourceGroup =~ \"my-rg\" and type =~ \"microsoft.network/virtualnetworks\"`",
            required=True,
        )
        export_query.recursive = AAZBoolArg(
            options=["recursive"],
            help="Whether to recursively list child resources of the query result",
            default=False,
        )

        export_resource = cls._args_schema.export_resource
        export_resource.name_pattern = AAZStrArg(
            options=["name-pattern"],
            help="The name pattern of the Terraform resources",
            default="res-",
        )
        export_resource.resource_ids = AAZListArg(
            options=["resource-ids"],
            help="The id of the resource to be exported",
            required=True,
        )
        export_resource.resource_name = AAZStrArg(
            options=["resource-name"],
            help="The Terraform resource name. Only works when `resourceIds` contains only one item.",
            default="res-0",
        )
        export_resource.resource_type = AAZStrArg(
            options=["resource-type"],
            help="The Terraform resource type. Only works when `resourceIds` contains only one item.",
        )

        resource_ids = cls._args_schema.export_resource.resource_ids
        resource_ids.Element = AAZStrArg()

        export_resource_group = cls._args_schema.export_resource_group
        export_resource_group.name_pattern = AAZStrArg(
            options=["name-pattern"],
            help="The name pattern of the Terraform resources",
            default="res-",
        )
        export_resource_group.resource_group_name = AAZStrArg(
            options=["resource-group-name"],
            help="The name of the resource group to be exported",
            required=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        yield self.ExportTerraform(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class ExportTerraform(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/providers/Microsoft.AzureTerraform/exportTerraform",
                **self.url_parameters
            )

        @property
        def method(self):
            return "POST"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-07-01-preview",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                typ=AAZObjectType,
                typ_kwargs={"flags": {"required": True, "client_flatten": True}}
            )
            _builder.set_prop("fullProperties", AAZBoolType, ".full_properties")
            _builder.set_prop("maskSensitive", AAZBoolType, ".mask_sensitive")
            _builder.set_prop("targetProvider", AAZStrType, ".target_provider")
            _builder.set_const("type", "ExportQuery", AAZStrType, ".export_query", typ_kwargs={"flags": {"required": True}})
            _builder.set_const("type", "ExportResource", AAZStrType, ".export_resource", typ_kwargs={"flags": {"required": True}})
            _builder.set_const("type", "ExportResourceGroup", AAZStrType, ".export_resource_group", typ_kwargs={"flags": {"required": True}})
            _builder.discriminate_by("type", "ExportQuery")
            _builder.discriminate_by("type", "ExportResource")
            _builder.discriminate_by("type", "ExportResourceGroup")

            disc_export_query = _builder.get("{type:ExportQuery}")
            if disc_export_query is not None:
                disc_export_query.set_prop("namePattern", AAZStrType, ".export_query.name_pattern")
                disc_export_query.set_prop("query", AAZStrType, ".export_query.query", typ_kwargs={"flags": {"required": True}})
                disc_export_query.set_prop("recursive", AAZBoolType, ".export_query.recursive")

            disc_export_resource = _builder.get("{type:ExportResource}")
            if disc_export_resource is not None:
                disc_export_resource.set_prop("namePattern", AAZStrType, ".export_resource.name_pattern")
                disc_export_resource.set_prop("resourceIds", AAZListType, ".export_resource.resource_ids", typ_kwargs={"flags": {"required": True}})
                disc_export_resource.set_prop("resourceName", AAZStrType, ".export_resource.resource_name")
                disc_export_resource.set_prop("resourceType", AAZStrType, ".export_resource.resource_type")

            resource_ids = _builder.get("{type:ExportResource}.resourceIds")
            if resource_ids is not None:
                resource_ids.set_elements(AAZStrType, ".")

            disc_export_resource_group = _builder.get("{type:ExportResourceGroup}")
            if disc_export_resource_group is not None:
                disc_export_resource_group.set_prop("namePattern", AAZStrType, ".export_resource_group.name_pattern")
                disc_export_resource_group.set_prop("resourceGroupName", AAZStrType, ".export_resource_group.resource_group_name", typ_kwargs={"flags": {"required": True}})

            return self.serialize_content(_content_value)

        def on_200_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200_201
            )

        _schema_on_200_201 = None

        @classmethod
        def _build_schema_on_200_201(cls):
            if cls._schema_on_200_201 is not None:
                return cls._schema_on_200_201

            cls._schema_on_200_201 = AAZObjectType()

            _schema_on_200_201 = cls._schema_on_200_201
            _schema_on_200_201.end_time = AAZStrType(
                serialized_name="endTime",
                flags={"read_only": True},
            )
            _schema_on_200_201.error = AAZObjectType()
            _ExportTerraformHelper._build_schema_error_detail_read(_schema_on_200_201.error)
            _schema_on_200_201.id = AAZStrType()
            _schema_on_200_201.name = AAZStrType()
            _schema_on_200_201.percent_complete = AAZFloatType(
                serialized_name="percentComplete",
            )
            _schema_on_200_201.properties = AAZObjectType()
            _schema_on_200_201.start_time = AAZStrType(
                serialized_name="startTime",
                flags={"read_only": True},
            )
            _schema_on_200_201.status = AAZStrType()

            properties = cls._schema_on_200_201.properties
            properties.configuration = AAZStrType()
            properties.errors = AAZListType()
            properties.skipped_resources = AAZListType(
                serialized_name="skippedResources",
            )

            errors = cls._schema_on_200_201.properties.errors
            errors.Element = AAZObjectType()
            _ExportTerraformHelper._build_schema_error_detail_read(errors.Element)

            skipped_resources = cls._schema_on_200_201.properties.skipped_resources
            skipped_resources.Element = AAZStrType()

            return cls._schema_on_200_201


class _ExportTerraformHelper:
    """Helper class for ExportTerraform"""

    _schema_error_detail_read = None

    @classmethod
    def _build_schema_error_detail_read(cls, _schema):
        if cls._schema_error_detail_read is not None:
            _schema.additional_info = cls._schema_error_detail_read.additional_info
            _schema.code = cls._schema_error_detail_read.code
            _schema.details = cls._schema_error_detail_read.details
            _schema.message = cls._schema_error_detail_read.message
            _schema.target = cls._schema_error_detail_read.target
            return

        cls._schema_error_detail_read = _schema_error_detail_read = AAZObjectType()

        error_detail_read = _schema_error_detail_read
        error_detail_read.additional_info = AAZListType(
            serialized_name="additionalInfo",
            flags={"read_only": True},
        )
        error_detail_read.code = AAZStrType(
            flags={"read_only": True},
        )
        error_detail_read.details = AAZListType(
            flags={"read_only": True},
        )
        error_detail_read.message = AAZStrType(
            flags={"read_only": True},
        )
        error_detail_read.target = AAZStrType(
            flags={"read_only": True},
        )

        additional_info = _schema_error_detail_read.additional_info
        additional_info.Element = AAZObjectType()

        _element = _schema_error_detail_read.additional_info.Element
        _element.info = AAZFreeFormDictType(
            flags={"read_only": True},
        )
        _element.type = AAZStrType(
            flags={"read_only": True},
        )

        details = _schema_error_detail_read.details
        details.Element = AAZObjectType()
        cls._build_schema_error_detail_read(details.Element)

        _schema.additional_info = cls._schema_error_detail_read.additional_info
        _schema.code = cls._schema_error_detail_read.code
        _schema.details = cls._schema_error_detail_read.details
        _schema.message = cls._schema_error_detail_read.message
        _schema.target = cls._schema_error_detail_read.target


__all__ = ["ExportTerraform"]
