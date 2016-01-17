#!/usr/bin/env python
 
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting

import sys
import os

import logging
import argparse

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
    
    logger.info('Used options: {0}'.format(args))
    logger.info('Called from ' + os.path.abspath(__file__) )

    os.chdir(os.path.dirname(os.path.abspath(__file__)) )

    server = BaseHTTPServer.HTTPServer
    handler = CGIHTTPServer.CGIHTTPRequestHandler
    server_address = ("", 8020)
    handler.cgi_directories = ["/cgi-bin"]

    httpd = server(server_address, handler)
    httpd.serve_forever()

