import logging
import sys
from functools import wraps

log = logging.getLogger(__name__)


def disable_for_loaddata(signal_handler):
    """
    Do not execute the signal when loading fixture data
    """
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get('raw'):
            log.debug("skipping signal when loading data")
            return
        signal_handler(*args, **kwargs)
    return wrapper

def disable_for_tests(signal_handler):
    """
    Do not execute when running django unittests
    """
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if sys.argv[1:2] == ['test']:
            log.debug("skipping signal when running unit tests")
            return
        signal_handler(*args, **kwargs)
    return wrapper

