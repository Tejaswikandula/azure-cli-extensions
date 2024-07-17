# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pylint: disable=too-many-statements
# pylint: disable=protected-access

import os
from knack.log import get_logger
from azure.cli.core.aaz import register_client, AAZClientConfiguration, has_value
from azure.cli.core.commands import LongRunningOperation
from azure.cli.core.aaz._client import AAZMgmtClient
from .utils import (
    GetClosestFullHour,
    ParseSubsFromResources,
    saveArrayAsCsv,
)
from .aaz.latest.acat import Onboard as _AcatOnboard
from .aaz.latest.acat import TriggerEvaluation as _AcatTriggerEvaluation
from .aaz.latest.acat.report import List as _AcatListReport
from .aaz.latest.acat.report import Show as _AcatShowReport
from .aaz.latest.acat.report import Create as _AcatCreateReport
from .aaz.latest.acat.report import Update as _AcatUpdateReport
from .aaz.latest.acat.report import Delete as _AcatDeleteReport
from .aaz.latest.acat.report.snapshot import (
    List as _AcatListSnapshot,
)
from .aaz.latest.acat.report.snapshot import (
    Download as _AcatDownloadSnapshot,
)
from .aaz.latest.acat.report.webhook import (
    List as _AcatListReportWebhook,
)
from .aaz.latest.acat.report.webhook import (
    Show as _AcatShowReportWebhook,
)
from .aaz.latest.acat.report.webhook import (
    Create as _AcatCreateReportWebhook,
)
from .aaz.latest.acat.report.webhook import (
    Update as _AcatUpdateReportWebhook,
)
from .aaz.latest.acat.report.webhook import (
    Delete as _AcatDeleteReportWebhook,
)

logger = get_logger(__name__)


@register_client("AcatMgmtClient")
class AAZAcatMgmtClient(AAZMgmtClient):
    @classmethod
    def _build_configuration(cls, ctx, credential, **kwargs):
        from azure.cli.core.auth.util import resource_to_scopes
        from azure.core.pipeline.policies import HeadersPolicy

        token = "Bearer " + credential.get_token().token
        headers_policy = HeadersPolicy(**kwargs)
        headers_policy.add_header("x-ms-aad-user-token", token)
        kwargs["headers_policy"] = headers_policy

        return AAZClientConfiguration(
            credential=credential,
            credential_scopes=resource_to_scopes(
                ctx.cli_ctx.cloud.endpoints.active_directory_resource_id
            ),
            **kwargs,
        )


class OnboardAcat(_AcatOnboard):
    class OnboardAcatWithDupAadToken(_AcatOnboard.ProviderActionsOnboard):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        yield self.OnboardAcatWithDupAadToken(ctx=self.ctx)()
        self.post_operations()


class TriggerEvaluation(_AcatTriggerEvaluation):

    class TriggerEvaluationWithDupAadToken(
        _AcatTriggerEvaluation.ProviderActionsTriggerEvaluation
    ):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        yield self.TriggerEvaluationWithDupAadToken(ctx=self.ctx)()
        self.post_operations()


class ListAcatReport(_AcatListReport):
    class ListAcatReportWithDupAadToken(_AcatListReport.ReportList):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        self.ListAcatReportWithDupAadToken(ctx=self.ctx)()
        self.post_operations()


class ShowAcatReport(_AcatShowReport):
    class ShowAcatReportWithDupAadToken(_AcatShowReport.ReportGet):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        self.ShowAcatReportWithDupAadToken(ctx=self.ctx)()
        self.post_operations()


class CreateAcatReport(_AcatCreateReport):
    class CreateAcatReportWithDupAadToken(_AcatCreateReport.ReportCreateOrUpdate):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        yield self.CreateAcatReportWithDupAadToken(ctx=self.ctx)()
        self.post_operations()

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        from azure.cli.core.aaz import AAZDateTimeArg

        args_schema.trigger_time_by_codegen._required = False
        args_schema.trigger_time_by_codegen._registered = False
        args_schema.trigger_time_with_default = AAZDateTimeArg(
            options=["--trigger-time"],
            arg_group="Properties",
            help="Report collection trigger time.",
            default=GetClosestFullHour(),
        )
        return args_schema

    def pre_operations(self):

        poller = OnboardAcat(cli_ctx=self.cli_ctx)(
            command_args={
                "subscription_ids": ParseSubsFromResources(self.ctx.args.resources),
            }
        )
        LongRunningOperation(self.cli_ctx)(poller)
        args = self.ctx.args
        args.trigger_time_by_codegen = args.trigger_time_with_default


class UpdateAcatReport(_AcatUpdateReport):
    class UpdateAcatReportWithDupAadToken(_AcatUpdateReport.ReportCreateOrUpdate):
        CLIENT_TYPE = "AcatMgmtClient"

    class GetAcatReportWithDupAadToken(_AcatUpdateReport.ReportGet):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        self.GetAcatReportWithDupAadToken(ctx=self.ctx)()
        self.pre_instance_update(self.ctx.vars.instance)
        self.InstanceUpdateByJson(ctx=self.ctx)()
        self.InstanceUpdateByGeneric(ctx=self.ctx)()
        self.post_instance_update(self.ctx.vars.instance)
        yield self.UpdateAcatReportWithDupAadToken(ctx=self.ctx)()
        self.post_operations()


class DeleteAcatReport(_AcatDeleteReport):
    class DeleteAcatReportWithDupAadToken(_AcatDeleteReport.ReportDelete):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        yield self.DeleteAcatReportWithDupAadToken(ctx=self.ctx)()
        self.post_operations()


class DownloadAcatReport(_AcatDownloadSnapshot):
    class DownloadAcatReportWithDupAadToken(_AcatDownloadSnapshot.SnapshotDownload):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        yield self.DownloadAcatReportWithDupAadToken(ctx=self.ctx)()
        self.post_operations()

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        from azure.cli.core.aaz import AAZStrArg

        args_schema = super()._build_arguments_schema(*args, **kwargs)
        args_schema.snapshot_name._required = False
        args_schema.snapshot_name._registered = False

        args_schema.path = AAZStrArg(
            options=["--path"],
            arg_group="Parameters",
            help="Path to the downloaded file",
            required=False,
        )
        args_schema.name = AAZStrArg(
            options=["--name"],
            arg_group="Parameters",
            help="Name of the downloaded file without postfix",
            required=False,
        )
        return args_schema

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)

        args = self.ctx.args
        downloadType = args.download_type.to_serialized_data()

        fullpath = os.path.join(
            args.path.to_serialized_data(), args.name.to_serialized_data()
        ) + (".pdf" if downloadType == "CompliancePdfReport" else ".csv")

        if downloadType == "CompliancePdfReport":
            import urllib.request

            urllib.request.urlretrieve(
                result["compliancePdfReport"]["sasUri"], fullpath
            )
        elif downloadType == "ComplianceReport":
            saveArrayAsCsv(result["complianceReport"], fullpath)
        elif downloadType == "ResourceList":
            saveArrayAsCsv(result["resourceList"], fullpath)
        else:
            raise NameError(f"Unsupported download type {downloadType}")
        return f"File downloaded at {fullpath}"

    def pre_operations(self):
        args = self.ctx.args
        pagedResult = GetControlAssessment(cli_ctx=self.cli_ctx)(
            command_args={"report_name": args.report_name, "compliance_status": "all"}
        )
        snapshot_name = None
        for result in pagedResult:
            snapshot_name = result["snapshotName"] if result is not None else None
            break
        if snapshot_name is None:
            raise ValueError(
                f"No snapshot found for report {self.ctx.args.report_name}"
            )
        args.snapshot_name = snapshot_name
        downloadType = args.download_type.to_serialized_data()

        if not has_value(args.path):
            args.path = os.getcwd()
        if not has_value(args.name):
            args.name = downloadType


class GetControlAssessment(_AcatListSnapshot):
    class GetControlAssessmentWithDupAadToken(_AcatListSnapshot.SnapshotList):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        self.GetControlAssessmentWithDupAadToken(ctx=self.ctx)()
        self.post_operations()

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)

        from azure.cli.core.aaz import AAZStrArg

        args_schema.compliance_status = AAZStrArg(
            options=["--compliance-status"],
            help="Compliance status.",
            enum={
                "failed": "Failed",
                "succeeded": "Passed",
                "na": "Not Applicable",
                "all": "Full Assessments",
            },
            default="Full Assessments",
        )
        return args_schema

    def _output(self, *args, **kwargs):
        snapshots = self.deserialize_output(
            self.ctx.vars.instance.value, client_flatten=True
        )
        next_link = self.deserialize_output(self.ctx.vars.instance.next_link)
        if len(snapshots) == 0:
            raise ValueError(
                f"No snapshot found for report {self.ctx.args.report_name}"
            )
        latestSnapshot = snapshots[0]
        if self.ctx.args.compliance_status == "Full Assessments":
            return [latestSnapshot], next_link
        filteredCategories = [
            {
                "categoryName": category["categoryName"],
                "categoryStatus": category["categoryStatus"],
                "controlFamilies": [
                    {
                        "controlFamilyName": controlFamily["controlFamilyName"],
                        "controlFamilyStatus": controlFamily["controlFamilyStatus"],
                        "controls": [
                            control
                            for control in controlFamily["controls"]
                            if control["controlStatus"]
                            == self.ctx.args.compliance_status
                        ],
                    }
                    for controlFamily in category["controlFamilies"]
                ],
            }
            for category in latestSnapshot["complianceResults"][0]["categories"]
        ]
        latestSnapshot["complianceResults"][0]["categories"] = filteredCategories
        return [latestSnapshot], next_link


class ListAcatReportWebhook(_AcatListReportWebhook):
    class ListAcatReportWebhookWithDupAadToken(_AcatListReportWebhook.WebhookList):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        self.ListAcatReportWebhookWithDupAadToken(ctx=self.ctx)()
        self.post_operations()


class ShowAcatReportWebhook(_AcatShowReportWebhook):
    class ShowAcatReportWebhookWithDupAadToken(_AcatShowReportWebhook.WebhookGet):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        self.ShowAcatReportWebhookWithDupAadToken(ctx=self.ctx)()
        self.post_operations()


class CreateAcatReportWebhook(_AcatCreateReportWebhook):
    class CreateAcatReportWebhookWithDupAadToken(
        _AcatCreateReportWebhook.WebhookCreateOrUpdate
    ):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        self.CreateAcatReportWebhookWithDupAadToken(ctx=self.ctx)()
        self.post_operations()

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        from azure.cli.core.aaz import AAZStrArg

        args_schema.payload_url._required = True
        args_schema.send_all_events._required = False
        args_schema.send_all_events._registered = False
        args_schema.status._required = False
        args_schema.status._registered = False
        args_schema.update_webhook_key._required = False
        args_schema.update_webhook_key._registered = False

        args_schema.trigger_mode = AAZStrArg(
            options=["--trigger-mode"],
            arg_group="Properties",
            help="whether to send notification under any event.",
            default="true",
            enum={"all": "true", "customize": "false"},
        )

        args_schema.status_with_default = AAZStrArg(
            options=["--disable"],
            arg_group="Properties",
            help="Webhook status.",
            enum={"false": "Enabled", "true": "Disabled"},
            default="Enalbed",
            blank="Disabled",
        )
        return args_schema

    def pre_operations(self):
        args = self.ctx.args
        args.status = args.status_with_default
        args.send_all_events = args.trigger_mode

        if has_value(args.secret):
            args.update_webhook_key = "true"
        else:
            args.secret = ""
            args.update_webhook_key = "false"


class UpdateAcatReportWebhook(_AcatUpdateReportWebhook):
    class UpdateAcatReportWebhookWithDupAadToken(
        _AcatUpdateReportWebhook.WebhookUpdate
    ):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        self.UpdateAcatReportWebhookWithDupAadToken(ctx=self.ctx)()
        self.post_operations()

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        from azure.cli.core.aaz import AAZStrArg

        args_schema.send_all_events._required = False
        args_schema.send_all_events._registered = False
        args_schema.status._required = False
        args_schema.status._registered = False
        args_schema.update_webhook_key._required = False
        args_schema.update_webhook_key._registered = False

        args_schema.trigger_mode = AAZStrArg(
            options=["--trigger-mode"],
            arg_group="Properties",
            help="whether to send notification under any event.",
            enum={"all": "true", "customize": "false"},
        )
        args_schema.status_nullable = AAZStrArg(
            options=["--disable"],
            arg_group="Properties",
            help="Webhook status.",
            nullable=True,
            enum={"false": "Enabled", "true": "Disabled"},
            blank="Disabled",
        )
        return args_schema

    def pre_operations(self):
        args = self.ctx.args
        args.status = args.status_nullable
        args.send_all_events = args.trigger_mode

        if has_value(args.secret):
            args.update_webhook_key = "true"
        else:
            args.update_webhook_key = "false"


class DeleteAcatReportWebhook(_AcatDeleteReportWebhook):
    class DeleteAcatReportWebhookWithDupAadToken(
        _AcatDeleteReportWebhook.WebhookDelete
    ):
        CLIENT_TYPE = "AcatMgmtClient"

    def _execute_operations(self):
        self.pre_operations()
        self.DeleteAcatReportWebhookWithDupAadToken(ctx=self.ctx)()
        self.post_operations()
