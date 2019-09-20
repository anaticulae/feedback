# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# ADD EXPERIMENTAL CODE HERE

import subprocess


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
