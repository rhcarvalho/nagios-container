#!/usr/bin/env python
import sys
import json
import argparse
import urllib2

import nagios


def generate_parser():
    parser = argparse.ArgumentParser(
        description="Checks the health endpoint of an RHMAP component",
    )
    parser.add_argument(
        "-H", "--host", required=True,
        help="host name of the component",
    )
    parser.add_argument(
        "-P", "--port", default="8080",
        help="port number of the component (default: %(default)s)",
    )
    parser.add_argument(
        "-E", "--endpoint", default="/sys/info/health",
        help="health endpoint (default: %(default)s)",
    )
    return parser


class RequestError(Exception):

    def __init__(self, message):
        self.message = message


def do_request(host, port, endpoint):
    url = 'http://%s:%s%s' % (host, port, endpoint)
    try:
        data = urllib2.urlopen(url).read()
    except urllib2.HTTPError as error:
        if error.code == 500:
            # For some reason the health endpoint returns a http status code of
            # 500 when the health isn't ok, so we have to check the http error
            # for a health response here
            try:
                data = error.read()
                json.loads(data)
            except ValueError:
                raise RequestError(error)
        else:
            raise RequestError(error)
    except urllib2.URLError as error:
        raise RequestError(
            'The health endpoint at "%s" is not contactable. Error: %s' %
            (url, error))
    return data


def parse_response(response):
    data = json.loads(response)
    if data['status'] == 'ok':
        nagios_status = nagios.OK
    elif data['status'] == 'warn':
        nagios_status = nagios.WARN
    elif data['status'] == 'crit':
        nagios_status = nagios.CRIT
    else:
        nagios_status = nagios.UNKNOWN
    return (nagios_status, data['summary'], data['details'])


def report(summary, test_results):
    print summary
    for test in test_results:
        print 'Test: %s - Status: %s - Details: %s' % (test['description'], test['test_status'], test['result'])


def main():
    try:
        args = generate_parser().parse_args()
        host = args.host
        port = args.port
        endpoint = args.endpoint
        response = do_request(host, port, endpoint)
        nagios_status, test_summary, test_results = parse_response(response)
        report(test_summary, test_results)
    except RequestError as error:
        print error.message
        nagios_status = nagios.CRIT
    except:
        print "Unexpected error: %s" % (sys.exc_info()[0])
        nagios_status = nagios.UNKNOWN
    sys.exit(nagios_status)

if __name__ == "__main__":
    main()
