#https://realpython.com/python-logging/

from module.lower import do_something
import logging
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--debug', help='debug flag for decreased logging level', action='store_true')
args = parser.parse_args()


logging.basicConfig(level=logging.WARNING,
                    #filename='basic_config_test1.log',                           #to a file
                    format='%(asctime)s %(name)s \t %(levelname)s:%(message)s')

if args.debug:
    logging.getLogger().setLevel(level=logging.DEBUG)

log = logging.getLogger(__name__)

log.warning('This is a warning')
log.debug('this is a debug message')

do_something()

