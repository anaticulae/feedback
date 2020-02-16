# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# ADD EXPERIMENTAL CODE HERE

import glob
import inspect
import os
import subprocess
import typing

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


def prepare_inputs(
        inputs: list,
        inspaces: list,
        outspace: str,
) -> typing.List[str]:
    """Parse single and multiple file input

    Locate files by defined pattern in `Workplan`. A file pattern is
    defined via (name, typ). The ext is in UPPER-CASES, for example (*,
    PDF) to locate multiple pdf's.

    Args:
        inputs(str): inputs are defined in a workplan
        inspaces(str): inspaces is the current input via -i
        outspace(str): path to write results and use as possible input
                       source for `recursive inputs`.
    Returns:
        List of located files.
    """

    utila.call('prepare inputs')
    result = []
    # single file input
    search_location = ' '.join(inspaces)
    for item in inputs:
        lastinput = item == inputs[-1]
        utila.info('skipping input `%s`, require `Pattern' % str(item))
        if not isinstance(item, utila.feature.Pattern):
            continue
        (name, ext) = item.name, item.ext
        for inspace in inspaces:
            if isinstance(item, utila.feature.ResultFile):
                producer = item.producer
                filename = '%s__%s.%s' % (producer, name, ext)
                filepath = os.path.join(inspace, filename)
                if os.path.exists(filepath):
                    result.append(filepath)
                    break  # do not double add path
                else:
                    # TODO: Refactor recursive inputs
                    # Only on the last inspace, because the file could exists
                    # in other input folder
                    if inspace == inspaces[-1]:
                        recursivepath = os.path.join(outspace, filename)
                        utila.info('recursive input %s' % recursivepath)
                        result.append('_%s' % recursivepath)
            elif isinstance(item, utila.feature.File):
                filename = '%s.%s' % (name, ext)
                filepath = os.path.join(inspace, filename)
                if os.path.exists(filepath):
                    result.append(filepath)
                    break  # do not double add path
                else:
                    if not lastinput:
                        continue
                    utila.error('search location: %s' % search_location)
                    utila.error('missing input: %s' % filepath)
            else:
                _, filename = os.path.split(inspace)
                if '.' in filename and filename[0] != '.':  # .tmp
                    # .tmp is not a file name, it is a directory.
                    # File as a input name
                    result.append(inspace)
                    break  # do not double add path
                elif os.path.isfile(inspace):
                    # support dir-like file-path as input
                    # TODO: Introduce new datatype?
                    result.append(inspace)
                    break  # do not double add path
                else:
                    ext = ext.lower()
                    pattern = '%s/%s.%s' % (inspace, name, ext)
                    utila.info('using pattern: %s' % pattern)
                    files = glob.glob(pattern)
                    utila.info('%s' % str(files))
                    for finding in files:
                        utila.log('FINDING %s' % finding)
                        result.append(finding)

    utila.call('result: %s\n' % result)
    return result


utila.feature.prepare_inputs = prepare_inputs
