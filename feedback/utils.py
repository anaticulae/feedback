# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# ADD EXPERIMENTAL CODE HERE

import inspect
import subprocess

import utila
import utila.feature


def format_completed(completed: subprocess.CompletedProcess) -> str:
    """Format stdout, stderr and returncode of completed process as
    process overview

    Args:
        completed(subprocess.Completed): completed process
    Returns:
        formated process
    Format:
        args: ...
        stdout: ...
        stderr: ...
        returncode: ...
    """
    stderr = completed.stderr if completed.stderr else 'stderr: empty!'
    stdout = completed.stdout if completed.stdout else 'stdout: empty!'
    msg = ('[process completed: start]\n'
           f'args: "{completed.args}"\n'
           f'stdout:\n{stdout}\n'
           f'stderr:\n{stderr}\n'
           f'returncode: {completed.returncode}\n'
           '[process completed: end]')
    return msg


def verify_interface(inputs, outputs, worker):
    # TODO: MOVE TO UTILA
    # TODO: EXTEND DOC
    # check callable
    # check input parameter
    call_parameter = inspect.signature(worker).parameters
    parameter = [str(item) for item in call_parameter.values()]
    # variable name of input parameter
    dynamic_collection = len([item for item in parameter if '*' in item]) == 1
    if not dynamic_collection:
        # Optional pages flag, reduces count of required parameter in
        # definition.
        has_pages = int(utila.PAGES_FLAG in call_parameter)
        if not len(call_parameter) == len(inputs) + has_pages:
            utila.error(
                f'missing input resources: '
                f'interface error {list(call_parameter.keys())} != {inputs}')
            return utila.FAILURE

    # check output parameter
    return_parameter = str(inspect.signature(worker).return_annotation)
    return_count = return_parameter.count('str')

    variable_returnvalues = utila.feature.variable_parameter(outputs)
    if not len(outputs) == return_count and not variable_returnvalues:
        utila.error(f'missing output resources: '
                    f'interface error {return_parameter} != {outputs}')
        return utila.FAILURE
    return utila.SUCCESS


utila.feature.verify_interface = verify_interface
