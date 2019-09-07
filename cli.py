#!/usr/bin/env python

import argparse
import telnetlib
import os
import sys
import time


class LutronSmartBridgePro:
    def __init__(self, host, port=23, quiet=False):
        self.session = None
        self.connection = None
        self.host = host
        self.port = port
        self.username = "lutron"
        self.password = "integration"
        self.quiet = quiet

    # doesn't wait for prompts, just expects they appear
    def login_sleep(self):
        self.connection = False
        self.session = telnetlib.Telnet(self.host, self.port)
        # self.session.set_debuglevel(4000000)
        while self.connection is False:
            print("Attempting to connect to Lutron Hub at %s" % (self.host))
            # self.session.read_until("login:")
            time.sleep(2)
            self.session.write("%s\r\n" % self.username)
            time.sleep(2)
            # self.session.read_until("password")
            self.session.write("%s\r\n" % self.password)
            self.session.read_until("GNET")
            self.connection = True
        if not self.quiet:
            print("Successfully Logged in to Lutron Hub")
        return True

    def login_wait(self):
        self.connection = False
        self.session = telnetlib.Telnet(self.host, self.port)
        # self.session.set_debuglevel(4000000)
        while self.connection is False:
            if not self.quiet:
                print("Attempting to connect to Lutron Hub at %s" % (self.host))
            self.session.read_until("login:")
            self.session.write("%s\r\n" % self.username)
            self.session.read_until("password")
            self.session.write("%s\r\n" % self.password)
            self.session.read_until("GNET")
            self.connection = True
        if not self.quiet:
            print("Successfully Logged in to Lutron Hub")
        return True

    def send_lutron_raw_command(self, raw_command):
        self.session.write("#{}\r\n".format(raw_command))
        return True

    def send_lutron_command(self, command, integration, action, parameters):
        self.session.write(
            "#{},{},{},{}\r\n".format(command, integration, action, parameters or 0)
        )
        return True


class Cli(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Interacts with a Lutron SmartBridge Pro"
        )
        self.parser.add_argument("--host")
        self.parser.add_argument(
            "-q", "--quiet", help="hide all output", action="store_true"
        )
        self.subparsers = self.parser.add_subparsers()

        parser_send = self.subparsers.add_parser("send")
        parser_send.add_argument("command")
        parser_send.add_argument("integration")
        parser_send.add_argument("action")
        parser_send.add_argument("parameters")
        parser_send.set_defaults(func=self.send)

        parser_send_raw = self.subparsers.add_parser("send_raw")
        parser_send_raw.add_argument("raw_command")
        parser_send_raw.set_defaults(func=self.send_raw)

        args = self.parser.parse_args()

        if "LUTRON_HOST" in os.environ:
            print("Using LUTRON_HOST env var for host (overriding --host)...")
            args.host = os.environ["LUTRON_HOST"]
        if not args.host:
            print("Please specify a host with --host or the LUTRON_HOST env var.")
            sys.exit(1)

        args.func(args)

    def send(self, args):
        lsbr = LutronSmartBridgePro(args.host, quiet=args.quiet)
        lsbr.login_wait()
        lsbr.send_lutron_command(
            args.command, args.integration, args.action, args.parameters
        )

    def send_raw(self, args):
        lsbr = LutronSmartBridgePro(args.host, quiet=args.quiet)
        lsbr.login_wait()
        lsbr.send_lutron_raw_command(args.raw_command)


if __name__ == "__main__":
    Cli()
