# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import FAILURE
from utila import logging
from utila import logging_error
from utila import logging_stacktrace
from utila.error import CANCELLED_BY_USER


def saveme(systemexit=True):
    """Protect against KeyboardInterrupt and beautify Exceptions

    Args:
        systemexit(bool): return exit value of quit with SystemExit
        user_function(callable): function which is invoked savely
    Returns:
        function-wrapper
    """

    def decorating_function(user_function):

        def wrapper(*args, **kwds):
            ret = None
            try:
                ret = user_function(*args, **kwds)
            except KeyboardInterrupt:
                logging('\nOperation cancelled by user')
                ret = CANCELLED_BY_USER
            except Exception as error:  # pylint: disable=broad-except
                logging_error(error)
                logging_stacktrace()
                ret = FAILURE
            if systemexit:
                exit(ret)
            return ret

        return wrapper

    return decorating_function
