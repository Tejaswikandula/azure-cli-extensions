# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import sys

from pkg_resources import parse_version
from knack.log import get_logger
from azext_confcom.config import (
    DEFAULT_REGO_FRAGMENTS,
    VIRTUAL_NODE_YAML_METADATA,
    VIRTUAL_NODE_YAML_ANNOTATIONS,
    VIRTUAL_NODE_YAML_POLICY,
)
from azext_confcom import os_util
from azext_confcom.template_util import (
    pretty_print_func,
    print_func,
    str_to_sha256,
    inject_policy_into_template,
    print_existing_policy_from_arm_template,
    print_existing_policy_from_yaml,
    deep_dict_update,
    filter_non_pod_resources,
    convert_to_pod_spec_helper,
)
from azext_confcom.init_checks import run_initial_docker_checks
from azext_confcom import security_policy
from azext_confcom.security_policy import OutputType
from azext_confcom.kata_proxy import KataPolicyGenProxy


logger = get_logger(__name__)


# pylint: disable=too-many-locals, too-many-branches
def acipolicygen_confcom(
    input_path: str,
    arm_template: str,
    arm_template_parameters: str,
    image_name: str,
    virtual_node_yaml_path: str,
    infrastructure_svn: str,
    tar_mapping_location: str,
    approve_wildcards: str = False,
    outraw: bool = False,
    outraw_pretty_print: bool = False,
    diff: bool = False,
    validate_sidecar: bool = False,
    save_to_file: str = None,
    debug_mode: bool = False,
    print_policy_to_terminal: bool = False,
    disable_stdio: bool = False,
    print_existing_policy: bool = False,
    faster_hashing: bool = False,
):

    if sum(map(bool, [input_path, arm_template, image_name, virtual_node_yaml_path])) != 1:
        error_out("Can only generate CCE policy from one source at a time")
    if sum(map(bool, [print_policy_to_terminal, outraw, outraw_pretty_print])) > 1:
        error_out("Can only print in one format at a time")
    elif (diff and input_path) or (diff and image_name):
        error_out("Can only diff CCE policy from ARM Template or YAML File")
    elif arm_template_parameters and not arm_template:
        error_out(
            "Can only use ARM Template Parameters if ARM Template is also present"
        )
    elif save_to_file and arm_template and not (print_policy_to_terminal or outraw or outraw_pretty_print):
        error_out("Must print policy to terminal when saving to file")
    elif faster_hashing and tar_mapping_location:
        error_out("Cannot use --faster-hashing with --tar")

    if print_existing_policy or outraw or outraw_pretty_print:
        logger.warning(
            "%s %s %s %s %s",
            "Secrets that are included in the provided arm template or configuration files ",
            "in the container env or cmd sections will be printed out with this flag.",
            "These are outputed secrets that you must protect. Be sure that you do not include these secrets in your",
            "source control. Also verify that no secrets are present in the logs of your command or script.",
            "For additional information, see http://aka.ms/clisecrets. \n",
        )

    if print_existing_policy and arm_template:
        print_existing_policy_from_arm_template(arm_template, arm_template_parameters)
        sys.exit(0)
    elif print_existing_policy and virtual_node_yaml_path:
        print_existing_policy_from_yaml(virtual_node_yaml_path)
        sys.exit(0)

    if debug_mode:
        logger.warning("WARNING: %s %s",
                       "Debug mode must only be used for debugging purposes. ",
                       "It should not be used for production systems.\n")

    tar_mapping = tar_mapping_validation(tar_mapping_location)

    output_type = get_output_type(outraw, outraw_pretty_print)

    container_group_policies = None

    # warn user that input infrastructure_svn is less than the configured default value
    check_infrastructure_svn(infrastructure_svn)

    # telling the user what operation we're doing
    logger.warning(
        "Generating security policy for %s: %s in %s",
        "ARM Template" if arm_template else "Image" if image_name else "Input File",
        input_path or arm_template or image_name or virtual_node_yaml_path,
        "base64"
        if output_type == security_policy.OutputType.DEFAULT
        else "clear text",
    )
    # error checking for making sure an input is provided is above
    if input_path:
        container_group_policies = security_policy.load_policy_from_file(
            input_path, debug_mode=debug_mode,
        )
    elif arm_template:
        container_group_policies = security_policy.load_policy_from_arm_template_file(
            infrastructure_svn,
            arm_template,
            arm_template_parameters,
            debug_mode=debug_mode,
            disable_stdio=disable_stdio,
            approve_wildcards=approve_wildcards,
        )
    elif image_name:
        container_group_policies = security_policy.load_policy_from_image_name(
            image_name, debug_mode=debug_mode, disable_stdio=disable_stdio
        )
    elif virtual_node_yaml_path:
        container_group_policies = security_policy.load_policy_from_virtual_node_yaml_file(
            virtual_node_yaml_path=virtual_node_yaml_path,
            debug_mode=debug_mode,
            disable_stdio=disable_stdio,
            approve_wildcards=approve_wildcards,
        )
        virtual_node_yaml = list(os_util.load_multiple_yaml_from_file(virtual_node_yaml_path))
        filtered_yaml = filter_non_pod_resources(virtual_node_yaml)

    exit_code = 0

    # standardize the output so we're only operating on arrays
    # this makes more sense than making the "from_file" and "from_image" outputting arrays
    # since they can only ever output a single image's policy
    if not isinstance(container_group_policies, list):
        container_group_policies = [container_group_policies]

    for count, policy in enumerate(container_group_policies):
        policy.populate_policy_content_for_all_images(
            individual_image=bool(image_name), tar_mapping=tar_mapping, faster_hashing=faster_hashing
        )

        if validate_sidecar:
            exit_code = validate_sidecar_in_policy(policy, output_type == security_policy.OutputType.PRETTY_PRINT)
        elif virtual_node_yaml_path and not (print_policy_to_terminal or outraw or outraw_pretty_print or diff):
            current_yaml = filtered_yaml[count]
            # find where this policy needs to go in the original file
            count_in_file = virtual_node_yaml.index(current_yaml)
            # use the reference this helper function returns to place the policy in the correct spot
            pod_item = convert_to_pod_spec_helper(current_yaml)
            # Metadata to be added to virtual node YAML
            needed_metadata = {
                VIRTUAL_NODE_YAML_METADATA: {
                    VIRTUAL_NODE_YAML_ANNOTATIONS: {
                        VIRTUAL_NODE_YAML_POLICY: policy.get_serialized_output(),
                    }
                }
            }

            # Update virtual node YAML with metadata
            deep_dict_update(needed_metadata, pod_item)
            # replace contents in the original file
            virtual_node_yaml[count_in_file] = current_yaml

            os_util.write_multiple_yaml_to_file(virtual_node_yaml_path, virtual_node_yaml)
        elif diff:
            exit_code = get_diff_outputs(policy, output_type == security_policy.OutputType.PRETTY_PRINT)
        elif arm_template and not (print_policy_to_terminal or outraw or outraw_pretty_print):
            result = inject_policy_into_template(arm_template, arm_template_parameters,
                                                 policy.get_serialized_output(), count)
            if result:
                # this is always going to be the unencoded policy
                print(str_to_sha256(policy.get_serialized_output(OutputType.RAW)))
                logger.info("CCE Policy successfully injected into ARM Template")
        else:
            # output to terminal
            print(f"{policy.get_serialized_output(output_type)}\n\n")
            # output to file
            if save_to_file:
                logger.warning(
                    "%s %s %s",
                    "(Deprecation Warning) the --save-to-file (-s) flag is deprecated ",
                    "and will be removed in a future release. ",
                    "Please print to the console and redirect to a file instead."
                )
                policy.save_to_file(save_to_file, output_type)

    sys.exit(exit_code)


def katapolicygen_confcom(
    yaml_path: str,
    config_map_file: str,
    outraw: bool = False,
    print_policy: bool = False,
    use_cached_files: bool = False,
    settings_file_name: str = None,
    rules_file_name: str = None,
    print_version: bool = False,
    containerd_pull: str = False,
    containerd_socket_path: str = None,
):
    kata_proxy = KataPolicyGenProxy()

    if not (yaml_path or print_version):
        error_out("Either --yaml-path or --print-version is required")

    output = kata_proxy.kata_genpolicy(
        yaml_path,
        config_map_file=config_map_file,
        outraw=outraw,
        print_policy=print_policy,
        use_cached_files=use_cached_files,
        settings_file_name=settings_file_name,
        rules_file_name=rules_file_name,
        print_version=print_version,
        containerd_pull=containerd_pull,
        containerd_socket_path=containerd_socket_path,
    )
    print(output)
    sys.exit(0)


def update_confcom(cmd, instance, tags=None):
    with cmd.update_context(instance) as c:
        c.set_param("tags", tags)
    return instance


def check_infrastructure_svn(infrastructure_svn):
    if infrastructure_svn and parse_version(infrastructure_svn) < parse_version(
        DEFAULT_REGO_FRAGMENTS[0]["minimum_svn"]
    ):
        logger.warning(
            "Input Infrastructure Fragment Software Version Number is less than the default Infrastructure SVN: %s",
            DEFAULT_REGO_FRAGMENTS[0]["minimum_svn"],
        )


def validate_sidecar_in_policy(policy: security_policy.AciPolicy, outraw_pretty_print: bool):
    is_valid, output = policy.validate_sidecars()

    if outraw_pretty_print:
        formatted_output = pretty_print_func(output)
    else:
        formatted_output = print_func(output)

    if is_valid:
        print("Sidecar containers will pass with its generated policy")
        return 0

    print(
        f"Sidecar containers will not pass with its generated policy: {formatted_output}"
    )
    return 2


def get_diff_outputs(policy: security_policy.AciPolicy, outraw_pretty_print: bool):
    exit_code = 0
    is_valid, output = policy.validate_cce_policy()

    if outraw_pretty_print:
        formatted_output = pretty_print_func(output)
    else:
        formatted_output = print_func(output)

    print(
        "Existing policy and Template match"
        if is_valid
        else formatted_output
    )
    fragment_diff = policy.compare_fragments()

    if fragment_diff != {}:
        logger.warning(
            "Fragments in the existing policy are not the defaults. If this is expected, ignore this warning."
        )
    if not is_valid:
        logger.warning(
            "Existing Policy and Template differ. Consider recreating the base64-encoded policy."
        )
        exit_code = 2
    return exit_code


def tar_mapping_validation(tar_mapping_location: str):
    tar_mapping = None
    if tar_mapping_location:
        if not os.path.isfile(tar_mapping_location):
            print(
                "--tar input must either be a path to a json file with "
                + "image to tar location mappings or the location to a single tar file."
            )
            sys.exit(2)
        # file is mapping images to tar file locations
        elif tar_mapping_location.endswith(".json"):
            tar_mapping = os_util.load_tar_mapping_from_file(tar_mapping_location)
        # passing in a single tar location for a single image policy
        else:
            tar_mapping = tar_mapping_location
    else:
        # only need to do the docker checks if we're not grabbing image info from tar files
        error_msg = run_initial_docker_checks()
        if error_msg:
            logger.warning(error_msg)
            sys.exit(1)
    return tar_mapping


def get_output_type(outraw, outraw_pretty_print):
    output_type = security_policy.OutputType.DEFAULT
    if outraw:
        output_type = security_policy.OutputType.RAW
    elif outraw_pretty_print:
        output_type = security_policy.OutputType.PRETTY_PRINT
    return output_type


def error_out(error_string):
    logger.error(error_string)
    sys.exit(1)
