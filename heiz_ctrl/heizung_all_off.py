#!/usr/bin/python

import sys
from time import sleep, strftime
from datetime import datetime, timedelta

import logging
import argparse

from heizctrl.ctrl import HeizungControl


if __name__ == '__main__':

    argparser = argparse.ArgumentParser()

    # Output verbosity options.
    argparser.add_argument('-q', '--quiet', help='set logging to ERROR',
                     action='store_const', dest='loglevel',
                     const=logging.ERROR, default=logging.INFO)
    argparser.add_argument('-d', '--debug', help='set logging to DEBUG',
                     action='store_const', dest='loglevel',
                     const=logging.DEBUG, default=logging.INFO)
    argparser.add_argument('-v', '--verbose', help='set logging to COMM',
                     action='store_const', dest='loglevel',
                     const=5, default=logging.INFO)

    argparser.add_argument("-l", "--logfile", dest="logfile",
                    help="logfile to use")

    argparser.add_argument("-i", "--init", action='store_true', dest="init",
                    help="Init hardware")

    args = argparser.parse_args()

    if args.logfile is not None:
        if sys.version_info < (3, 0):
            console_log = open(args.logfile, 'a', 1)
        else:
            console_log = open(args.logfile, 'a', 1, encoding='utf-8')
        sys.stdout = console_log
        sys.stderr = console_log

    # Setup logging.
    logging.basicConfig(level = args.loglevel, datefmt='%H:%M:%S', format='%(asctime)s %(levelname)s:%(name)s:%(funcName)s:%(message)s')
    logger = logging.getLogger(__name__)

    logger.debug('Used options: {0}'.format(args))

    # The hardware need to be init one time after boot. To do this, run this 
    # programm at boot with -i
    if args.init is not None:
        init = True
    else:
        init = False

    heizung = HeizungControl(init_board=init, logger=logger)
    heizung.heizung_all_off()


