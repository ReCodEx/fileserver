#!/usr/bin/env python3

from jinja2 import Template
from argparse import ArgumentParser
import os
import sys

args_parser = ArgumentParser()
subparsers = args_parser.add_subparsers(dest="server_type")

apache_parser = subparsers.add_parser("apache", help="Configure the fileserver as an Apache VirtualHost")
apache_parser.add_argument("--port", default=8080, type=int, dest="port", help="port where the fileserver should listen")
apache_parser.add_argument("--working-directory", required=True, type=str, dest="working_directory",
                           help="directory where the files should be stored")
apache_parser.add_argument("--htpasswd", type=str, dest="htpasswd", help="user file for HTTP basic auth")
apache_parser.add_argument("--user", dest="user", help="user under which the server should be run")


def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    args = args_parser.parse_args()
    script_dir = os.path.dirname(os.path.realpath(__file__))

    if args.server_type == "apache":
        with open(os.path.join(script_dir, "templates", "apache.conf")) as template_file:
            template = Template(template_file.read())

        print(template.render(
            working_directory=args.working_directory,
            install_directory=os.path.dirname(script_dir),
            port=args.port,
            htpasswd=args.htpasswd,
            user=args.user
        ))
    else:
        die("no action specified")
