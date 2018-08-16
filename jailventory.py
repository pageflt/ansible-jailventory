#!/usr/local/bin/python2.7

# Ansible dynamic inventory provider for FreeBSD jails. Details:
# https://docs.ansible.com/ansible/2.6/dev_guide/developing_inventory.html
#
# Dimitris Karagkasidis, <t.pagef.lt@gmail.com>
# https://github.com/pageflt/freebsd-vps-ops

import sys
from json import dumps
from argparse import ArgumentParser
from subprocess import check_output
from collections import namedtuple

hosts = {}
groups = {
  "jails": {
    "hosts": [],
    "vars": {
      "ansible_python_interpreter": "/usr/local/bin/python2.7",
    }
  }
}

def compile_inventory():
    # Compile an inventory of running jails by quering jls(8). 
    try:
        Jail = namedtuple('Jail', 'jid ip_address hostname path'.split())
        for j in check_output(['jls']).split("\n")[1:-1]:
            jail = Jail(*j.split())
            groups['jails']['hosts'].append(jail.hostname)
            hosts[jail.hostname] = { 'ansible_host': jail.ip_address }

    except Exception as Ex:
        raise Exception("get_jails(): %s" % Ex)

    
def parse_args():
    # Parse command-line arguments.
    try:
        parser = ArgumentParser(description='Ansible dynamic inventory \
                                             provider for FreeBSD jails')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--list", action="store_true")
        group.add_argument("--host", metavar='HOST', type=str)
        return parser.parse_args()

    except Exception as Ex:
        raise Exception("parse_args(): %s" % Ex)


def main():
    try:
        args = parse_args()
        compile_inventory()

        if args.list:
            sys.stdout.write(dumps(groups))
        else:
            sys.stdout.write(dumps(hosts[args.host]) if args.host in hosts
                                                     else "{}")
        return 0

    except Exception as Ex:
        sys.stderr.write("error: %s" % Ex)
        return 1


if __name__ == "__main__":
    sys.exit(main())

