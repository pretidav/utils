import logging


log = logging.getLogger(__name__)

def do_something():
    log.warning("Doing something!")
    log.debug('this is a debug from lower')