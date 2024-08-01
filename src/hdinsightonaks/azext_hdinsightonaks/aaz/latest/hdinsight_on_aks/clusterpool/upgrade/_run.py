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
    "hdinsight-on-aks clusterpool upgrade run",
    is_preview=True,
)
class Run(AAZCommand):
    """Upgrade a cluster pool.

    :example: Upgrade a cluster pool.
        az hdinsight-on-aks clusterpool upgrade run --cluster-pool-name {poolName} -g {RG} --upgrade-profile {target-aks-version=1.27.9 upgrade-clusters=false upgrade-cluster-pool=true}
    """

    _aaz_info = {
        "version": "2024-05-01-preview",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.hdinsight/clusterpools/{}/upgrade", "2024-05-01-preview"],
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

        _args_schema = cls._args_schema
        _args_schema.cluster_pool_name = AAZStrArg(
            options=["-n", "--name", "--cluster-pool-name"],
            help="The name of the cluster pool.",
            required=True,
            id_part="name",
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.upgrade_profile = AAZObjectArg(
            options=["--upgrade-profile"],
            arg_group="Properties",
            help="Define upgrade properties.",
        )
        _args_schema.node_os_upgrade = AAZObjectArg(
            options=["--node-os-upgrade"],
            arg_group="Properties",
            blank={},
        )

        upgrade_profile = cls._args_schema.upgrade_profile
        upgrade_profile.target_aks_version = AAZStrArg(
            options=["target-aks-version"],
            help="Target AKS version. When it's not set, latest version will be used. When upgradeClusterPool is true and upgradeAllClusterNodes is false, target version should be greater or equal to current version. When upgradeClusterPool is false and upgradeAllClusterNodes is true, target version should be equal to AKS version of cluster pool.",
        )
        upgrade_profile.upgrade_clusters = AAZBoolArg(
            options=["upgrade-clusters"],
            help="whether upgrade all clusters' nodes. If it's true, upgradeClusterPool should be false.",
            default=False,
        )
        upgrade_profile.upgrade_cluster_pool = AAZBoolArg(
            options=["upgrade-cluster-pool"],
            help="whether upgrade cluster pool or not. If it's true, upgradeAllClusterNodes should be false.",
            default=False,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        yield self.ClusterPoolsUpgrade(ctx=self.ctx)()
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

    class ClusterPoolsUpgrade(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200,
                    self.on_error,
                    lro_options={"final-state-via": "location"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200,
                    self.on_error,
                    lro_options={"final-state-via": "location"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HDInsight/clusterpools/{clusterPoolName}/upgrade",
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
                    "clusterPoolName", self.ctx.args.cluster_pool_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
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
                    "api-version", "2024-05-01-preview",
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
            _builder.set_prop("properties", AAZObjectType, ".", typ_kwargs={"flags": {"required": True}})

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_const("upgradeType", "AKSPatchUpgrade", AAZStrType, ".upgrade_profile", typ_kwargs={"flags": {"required": True}})
                properties.set_const("upgradeType", "NodeOsUpgrade", AAZStrType, ".node_os_upgrade", typ_kwargs={"flags": {"required": True}})
                properties.discriminate_by("upgradeType", "AKSPatchUpgrade")
                properties.discriminate_by("upgradeType", "NodeOsUpgrade")

            disc_aks_patch_upgrade = _builder.get(".properties{upgradeType:AKSPatchUpgrade}")
            if disc_aks_patch_upgrade is not None:
                disc_aks_patch_upgrade.set_prop("targetAksVersion", AAZStrType, ".upgrade_profile.target_aks_version")
                disc_aks_patch_upgrade.set_prop("upgradeAllClusterNodes", AAZBoolType, ".upgrade_profile.upgrade_clusters")
                disc_aks_patch_upgrade.set_prop("upgradeClusterPool", AAZBoolType, ".upgrade_profile.upgrade_cluster_pool")

            return self.serialize_content(_content_value)

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _schema_on_200.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200.tags = AAZDictType()
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties
            properties.aks_cluster_profile = AAZObjectType(
                serialized_name="aksClusterProfile",
                flags={"read_only": True},
            )
            properties.aks_managed_resource_group_name = AAZStrType(
                serialized_name="aksManagedResourceGroupName",
                flags={"read_only": True},
            )
            properties.cluster_pool_profile = AAZObjectType(
                serialized_name="clusterPoolProfile",
            )
            properties.compute_profile = AAZObjectType(
                serialized_name="computeProfile",
                flags={"required": True},
            )
            properties.deployment_id = AAZStrType(
                serialized_name="deploymentId",
                flags={"read_only": True},
            )
            properties.log_analytics_profile = AAZObjectType(
                serialized_name="logAnalyticsProfile",
            )
            properties.managed_resource_group_name = AAZStrType(
                serialized_name="managedResourceGroupName",
            )
            properties.network_profile = AAZObjectType(
                serialized_name="networkProfile",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.status = AAZStrType(
                flags={"read_only": True},
            )

            aks_cluster_profile = cls._schema_on_200.properties.aks_cluster_profile
            aks_cluster_profile.aks_cluster_agent_pool_identity_profile = AAZObjectType(
                serialized_name="aksClusterAgentPoolIdentityProfile",
            )
            aks_cluster_profile.aks_cluster_resource_id = AAZStrType(
                serialized_name="aksClusterResourceId",
            )
            aks_cluster_profile.aks_version = AAZStrType(
                serialized_name="aksVersion",
                flags={"read_only": True},
            )

            aks_cluster_agent_pool_identity_profile = cls._schema_on_200.properties.aks_cluster_profile.aks_cluster_agent_pool_identity_profile
            aks_cluster_agent_pool_identity_profile.msi_client_id = AAZStrType(
                serialized_name="msiClientId",
                flags={"required": True},
            )
            aks_cluster_agent_pool_identity_profile.msi_object_id = AAZStrType(
                serialized_name="msiObjectId",
                flags={"required": True},
            )
            aks_cluster_agent_pool_identity_profile.msi_resource_id = AAZStrType(
                serialized_name="msiResourceId",
                flags={"required": True},
            )

            cluster_pool_profile = cls._schema_on_200.properties.cluster_pool_profile
            cluster_pool_profile.cluster_pool_version = AAZStrType(
                serialized_name="clusterPoolVersion",
                flags={"required": True},
            )

            compute_profile = cls._schema_on_200.properties.compute_profile
            compute_profile.availability_zones = AAZListType(
                serialized_name="availabilityZones",
            )
            compute_profile.count = AAZIntType(
                flags={"read_only": True},
            )
            compute_profile.vm_size = AAZStrType(
                serialized_name="vmSize",
                flags={"required": True},
            )

            availability_zones = cls._schema_on_200.properties.compute_profile.availability_zones
            availability_zones.Element = AAZStrType()

            log_analytics_profile = cls._schema_on_200.properties.log_analytics_profile
            log_analytics_profile.enabled = AAZBoolType(
                flags={"required": True},
            )
            log_analytics_profile.workspace_id = AAZStrType(
                serialized_name="workspaceId",
            )

            network_profile = cls._schema_on_200.properties.network_profile
            network_profile.api_server_authorized_ip_ranges = AAZListType(
                serialized_name="apiServerAuthorizedIpRanges",
            )
            network_profile.enable_private_api_server = AAZBoolType(
                serialized_name="enablePrivateApiServer",
            )
            network_profile.outbound_type = AAZStrType(
                serialized_name="outboundType",
            )
            network_profile.subnet_id = AAZStrType(
                serialized_name="subnetId",
                flags={"required": True},
            )

            api_server_authorized_ip_ranges = cls._schema_on_200.properties.network_profile.api_server_authorized_ip_ranges
            api_server_authorized_ip_ranges.Element = AAZStrType()

            system_data = cls._schema_on_200.system_data
            system_data.created_at = AAZStrType(
                serialized_name="createdAt",
            )
            system_data.created_by = AAZStrType(
                serialized_name="createdBy",
            )
            system_data.created_by_type = AAZStrType(
                serialized_name="createdByType",
            )
            system_data.last_modified_at = AAZStrType(
                serialized_name="lastModifiedAt",
            )
            system_data.last_modified_by = AAZStrType(
                serialized_name="lastModifiedBy",
            )
            system_data.last_modified_by_type = AAZStrType(
                serialized_name="lastModifiedByType",
            )

            tags = cls._schema_on_200.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200


class _RunHelper:
    """Helper class for Run"""


__all__ = ["Run"]
