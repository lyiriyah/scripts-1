#!/usr/bin/env python3
""" get_public_ip.py
This module finds the outside IP address of the current host.

It's intended to be used as an i3blocks command, so at most this program
should output exactly one line to stdout.
"""

import sys
import argparse
import socket
from contextlib import contextmanager

@contextmanager
def open_tcp_connection(host, port, version=6):
    """Attempt to connect to host on port over TCP.

    Args:
        host (str): The address of the host to connect to.
        port (int): The port to connect to on host.
        version (int): Internet Protocol version to use.

    Yield (socket.socket) on success, False otherwise
    """
    if version == 4:
        sock = socket.socket(family=socket.AF_INET)
    else:
        sock = socket.socket(family=socket.AF_INET6)

    try:
        sock.connect((host, port))
    except OSError:
        sock = False

    yield sock

    if sock:
        sock.close()

def get_public_ip(version=6):
    """Return the outside IP address of this host as a string using the
    icanhazip.com service.

    Args:
        version (int): The Internet Protocol version number to find.

    Return (str or None): An IP address string.
    """
    with open_tcp_connection('icanhazip.com', 80, version) as sock:
        if not sock:
            return None
        sock.send(b'GET / HTTP/1.1\r\nHost: icanhazip.com\r\n\r\n')
        message = sock.recv(2048)

    result = str(message, encoding='utf-8').splitlines()[-1]
    return result

def main(argv):
    """Program entry point

    Args:
        argv (list): Unparsed arguments passed to program
    """
    parser = argparse.ArgumentParser(
        description='Print the public IP address of this host',
        epilog=('If --auto is specified, first attempt to retrieve IPv6 '
                'address. Then fall back to IPv4 if that fails. If no option '
                'is specified, --auto is assumed.')
        )
    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument(
        '-a', '--auto', action='store_const', const=0, dest='ip_version',
        default=0)
    version_group.add_argument(
        '-4', '--ipv4', action='store_const', const=4, dest='ip_version')
    version_group.add_argument(
        '-6', '--ipv6', action='store_const', const=6, dest='ip_version')
    parser.add_argument(
        '-f', '--failure_message', type=str, default='service unreachable')
    args = parser.parse_args(argv)

    if args.ip_version == 0:
        for version in [6, 4]:
            address = get_public_ip(version)
            if address:
                break
        else:
            address = args.failure_message
    else:
        address = get_public_ip(args.ip_version) or args.failure_message

    print('{}'.format(address))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))