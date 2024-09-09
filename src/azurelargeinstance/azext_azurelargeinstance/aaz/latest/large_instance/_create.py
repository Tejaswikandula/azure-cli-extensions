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
    "large-instance create",
)
class Create(AAZCommand):
    """Create an Azure Large Instance for the specified subscription,
resource group, and instance name.

    :example: AzureLargeInstance_Create
        az large-instance create -g myResourceGroup -n myALInstance -l westus --tags "{testkey:testvalue}" --instance-id 23415635-4d7e-41dc-9598-8194f22c24e1 --power-state started --ppg /subscriptions/f0f4887f-d13c-4943-a8ba-d7da28d2a3fd/resourceGroups/myResourceGroup/providers/Microsoft.Compute/proximityPlacementGroups/myplacementgroup --hw-revision Rev 3 --hardware-profile "{hardware-type:Cisco_UCS,azure-large-instance-size:S72}" --network-profile "{network-interfaces:[{ip-address:100.100.100.100}],circuit-id:/subscriptions/f0f4887f-d13c-4943-a8ba-d7da28d2a3fd/resourceGroups/myResourceGroup/providers/Microsoft.Network/expressRouteCircuit}" --storage-profile "{nfs-ip-address:200.200.200.200}" --os-profile "{computer-name:myComputerName,os-type:SUSE,version:'12 SP1',ssh-public-key:'{ssh-rsa public key}'}"
    """

    _aaz_info = {
        "version": "2024-08-01-preview",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.azurelargeinstance/azurelargeinstances/{}", "2024-08-01-preview"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.instance_name = AAZStrArg(
            options=["-n", "--name", "--instance-name"],
            help="Name of the AzureLargeInstance.",
            required=True,
            fmt=AAZStrArgFormat(
                pattern=".*",
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.instance_id = AAZStrArg(
            options=["--ali-id", "--instance-id"],
            arg_group="Properties",
            help="Specifies the Azure Large Instance unique ID.",
        )
        _args_schema.hardware_profile = AAZObjectArg(
            options=["--hardware-profile"],
            arg_group="Properties",
            help="Specifies the hardware settings for the Azure Large Instance.",
        )
        _args_schema.hw_revision = AAZStrArg(
            options=["--hw-revision"],
            arg_group="Properties",
            help="Hardware revision of an Azure Large Instance",
        )
        _args_schema.network_profile = AAZObjectArg(
            options=["--network-profile"],
            arg_group="Properties",
            help="Specifies the network settings for the Azure Large Instance.",
        )
        _args_schema.os_profile = AAZObjectArg(
            options=["--os-profile"],
            arg_group="Properties",
            help="Specifies the operating system settings for the Azure Large Instance.",
        )
        _args_schema.power_state = AAZStrArg(
            options=["--power-state"],
            arg_group="Properties",
            help="Resource power state",
            enum={"restarting": "restarting", "started": "started", "starting": "starting", "stopped": "stopped", "stopping": "stopping", "unknown": "unknown"},
        )
        _args_schema.proximity_placement_group = AAZStrArg(
            options=["--ppg", "--proximity-placement-group"],
            arg_group="Properties",
            help="Resource proximity placement group",
        )
        _args_schema.storage_profile = AAZObjectArg(
            options=["--storage-profile"],
            arg_group="Properties",
            help="Specifies the storage settings for the Azure Large Instance disks.",
        )

        hardware_profile = cls._args_schema.hardware_profile
        hardware_profile.azure_large_instance_size = AAZStrArg(
            options=["azure-large-instance-size"],
            help="Specifies the Azure Large Instance SKU.",
            enum={"S112": "S112", "S144": "S144", "S144m": "S144m", "S192": "S192", "S192m": "S192m", "S192xm": "S192xm", "S224": "S224", "S224m": "S224m", "S224om": "S224om", "S224oo": "S224oo", "S224oom": "S224oom", "S224ooo": "S224ooo", "S224se": "S224se", "S384": "S384", "S384m": "S384m", "S384xm": "S384xm", "S384xxm": "S384xxm", "S448": "S448", "S448m": "S448m", "S448om": "S448om", "S448oo": "S448oo", "S448oom": "S448oom", "S448ooo": "S448ooo", "S448se": "S448se", "S576m": "S576m", "S576xm": "S576xm", "S672": "S672", "S672m": "S672m", "S672om": "S672om", "S672oo": "S672oo", "S672oom": "S672oom", "S672ooo": "S672ooo", "S72": "S72", "S72m": "S72m", "S768": "S768", "S768m": "S768m", "S768xm": "S768xm", "S896": "S896", "S896m": "S896m", "S896om": "S896om", "S896oo": "S896oo", "S896oom": "S896oom", "S896ooo": "S896ooo", "S96": "S96", "S960m": "S960m"},
        )
        hardware_profile.hardware_type = AAZStrArg(
            options=["hardware-type"],
            help="Name of the hardware type (vendor and/or their product name)",
            enum={"Cisco_UCS": "Cisco_UCS", "HPE": "HPE", "SDFLEX": "SDFLEX"},
        )

        network_profile = cls._args_schema.network_profile
        network_profile.circuit_id = AAZStrArg(
            options=["circuit-id"],
            help="Specifies the circuit id for connecting to express route.",
        )
        network_profile.network_interfaces = AAZListArg(
            options=["network-interfaces"],
            help="Specifies the network interfaces for the Azure Large Instance.",
        )

        network_interfaces = cls._args_schema.network_profile.network_interfaces
        network_interfaces.Element = AAZObjectArg()

        _element = cls._args_schema.network_profile.network_interfaces.Element
        _element.ip_address = AAZStrArg(
            options=["ip-address"],
            help="Specifies the IP address of the network interface.",
        )

        os_profile = cls._args_schema.os_profile
        os_profile.computer_name = AAZStrArg(
            options=["computer-name"],
            help="Specifies the host OS name of the Azure Large Instance.",
        )
        os_profile.os_type = AAZStrArg(
            options=["os-type"],
            help="This property allows you to specify the type of the OS.",
        )
        os_profile.ssh_public_key = AAZStrArg(
            options=["ssh-public-key"],
            help="Specifies the SSH public key used to access the operating system.",
        )
        os_profile.version = AAZStrArg(
            options=["version"],
            help="Specifies version of operating system.",
        )

        storage_profile = cls._args_schema.storage_profile
        storage_profile.nfs_ip_address = AAZStrArg(
            options=["nfs-ip-address"],
            help="IP Address to connect to storage.",
        )
        storage_profile.os_disks = AAZListArg(
            options=["os-disks"],
            help="Specifies information about the operating system disk used by Azure Large Instance.",
        )

        os_disks = cls._args_schema.storage_profile.os_disks
        os_disks.Element = AAZObjectArg()

        _element = cls._args_schema.storage_profile.os_disks.Element
        _element.disk_size_gb = AAZIntArg(
            options=["disk-size-gb"],
            help="Specifies the size of an empty data disk in gigabytes.",
        )
        _element.name = AAZStrArg(
            options=["name"],
            help="The disk name.",
        )

        # define Arg Group "Resource"

        _args_schema = cls._args_schema
        _args_schema.location = AAZResourceLocationArg(
            arg_group="Resource",
            help="The geo-location where the resource lives",
            required=True,
            fmt=AAZResourceLocationArgFormat(
                resource_group_arg="resource_group",
            ),
        )
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            arg_group="Resource",
            help="Resource tags.",
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg()
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.AzureLargeInstanceCreate(ctx=self.ctx)()
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

    class AzureLargeInstanceCreate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200, 201]:
                return self.on_200_201(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.AzureLargeInstance/azureLargeInstances/{azureLargeInstanceName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "azureLargeInstanceName", self.ctx.args.instance_name,
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
                    "api-version", "2024-08-01-preview",
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
            _builder.set_prop("location", AAZStrType, ".location", typ_kwargs={"flags": {"required": True}})
            _builder.set_prop("properties", AAZObjectType, typ_kwargs={"flags": {"client_flatten": True}})
            _builder.set_prop("tags", AAZDictType, ".tags")

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("azureLargeInstanceId", AAZStrType, ".instance_id")
                properties.set_prop("hardwareProfile", AAZObjectType, ".hardware_profile")
                properties.set_prop("hwRevision", AAZStrType, ".hw_revision")
                properties.set_prop("networkProfile", AAZObjectType, ".network_profile")
                properties.set_prop("osProfile", AAZObjectType, ".os_profile")
                properties.set_prop("powerState", AAZStrType, ".power_state")
                properties.set_prop("proximityPlacementGroup", AAZStrType, ".proximity_placement_group")
                properties.set_prop("storageProfile", AAZObjectType, ".storage_profile")

            hardware_profile = _builder.get(".properties.hardwareProfile")
            if hardware_profile is not None:
                hardware_profile.set_prop("azureLargeInstanceSize", AAZStrType, ".azure_large_instance_size")
                hardware_profile.set_prop("hardwareType", AAZStrType, ".hardware_type")

            network_profile = _builder.get(".properties.networkProfile")
            if network_profile is not None:
                network_profile.set_prop("circuitId", AAZStrType, ".circuit_id")
                network_profile.set_prop("networkInterfaces", AAZListType, ".network_interfaces")

            network_interfaces = _builder.get(".properties.networkProfile.networkInterfaces")
            if network_interfaces is not None:
                network_interfaces.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.networkProfile.networkInterfaces[]")
            if _elements is not None:
                _elements.set_prop("ipAddress", AAZStrType, ".ip_address")

            os_profile = _builder.get(".properties.osProfile")
            if os_profile is not None:
                os_profile.set_prop("computerName", AAZStrType, ".computer_name")
                os_profile.set_prop("osType", AAZStrType, ".os_type")
                os_profile.set_prop("sshPublicKey", AAZStrType, ".ssh_public_key")
                os_profile.set_prop("version", AAZStrType, ".version")

            storage_profile = _builder.get(".properties.storageProfile")
            if storage_profile is not None:
                storage_profile.set_prop("nfsIpAddress", AAZStrType, ".nfs_ip_address")
                storage_profile.set_prop("osDisks", AAZListType, ".os_disks")

            os_disks = _builder.get(".properties.storageProfile.osDisks")
            if os_disks is not None:
                os_disks.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.storageProfile.osDisks[]")
            if _elements is not None:
                _elements.set_prop("diskSizeGB", AAZIntType, ".disk_size_gb")
                _elements.set_prop("name", AAZStrType, ".name")

            tags = _builder.get(".tags")
            if tags is not None:
                tags.set_elements(AAZStrType, ".")

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
            _schema_on_200_201.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200_201.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _schema_on_200_201.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200_201.tags = AAZDictType()
            _schema_on_200_201.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200_201.properties
            properties.azure_large_instance_id = AAZStrType(
                serialized_name="azureLargeInstanceId",
            )
            properties.hardware_profile = AAZObjectType(
                serialized_name="hardwareProfile",
            )
            properties.hw_revision = AAZStrType(
                serialized_name="hwRevision",
            )
            properties.network_profile = AAZObjectType(
                serialized_name="networkProfile",
            )
            properties.os_profile = AAZObjectType(
                serialized_name="osProfile",
            )
            properties.power_state = AAZStrType(
                serialized_name="powerState",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.proximity_placement_group = AAZStrType(
                serialized_name="proximityPlacementGroup",
            )
            properties.storage_profile = AAZObjectType(
                serialized_name="storageProfile",
            )

            hardware_profile = cls._schema_on_200_201.properties.hardware_profile
            hardware_profile.azure_large_instance_size = AAZStrType(
                serialized_name="azureLargeInstanceSize",
            )
            hardware_profile.hardware_type = AAZStrType(
                serialized_name="hardwareType",
            )

            network_profile = cls._schema_on_200_201.properties.network_profile
            network_profile.circuit_id = AAZStrType(
                serialized_name="circuitId",
            )
            network_profile.network_interfaces = AAZListType(
                serialized_name="networkInterfaces",
            )

            network_interfaces = cls._schema_on_200_201.properties.network_profile.network_interfaces
            network_interfaces.Element = AAZObjectType()

            _element = cls._schema_on_200_201.properties.network_profile.network_interfaces.Element
            _element.ip_address = AAZStrType(
                serialized_name="ipAddress",
            )

            os_profile = cls._schema_on_200_201.properties.os_profile
            os_profile.computer_name = AAZStrType(
                serialized_name="computerName",
            )
            os_profile.os_type = AAZStrType(
                serialized_name="osType",
            )
            os_profile.ssh_public_key = AAZStrType(
                serialized_name="sshPublicKey",
            )
            os_profile.version = AAZStrType()

            storage_profile = cls._schema_on_200_201.properties.storage_profile
            storage_profile.nfs_ip_address = AAZStrType(
                serialized_name="nfsIpAddress",
            )
            storage_profile.os_disks = AAZListType(
                serialized_name="osDisks",
            )

            os_disks = cls._schema_on_200_201.properties.storage_profile.os_disks
            os_disks.Element = AAZObjectType()

            _element = cls._schema_on_200_201.properties.storage_profile.os_disks.Element
            _element.disk_size_gb = AAZIntType(
                serialized_name="diskSizeGB",
            )
            _element.lun = AAZIntType(
                flags={"read_only": True},
            )
            _element.name = AAZStrType()

            system_data = cls._schema_on_200_201.system_data
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

            tags = cls._schema_on_200_201.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200_201


class _CreateHelper:
    """Helper class for Create"""


__all__ = ["Create"]
