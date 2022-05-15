#!/usr/bin/env python3

import argparse
from function_update import update_function

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Yandex Cloud functions wrapper'
    )
    subparsers = parser.add_subparsers(dest='command')

    update_parser = subparsers.add_parser(
        name='function-update',
        description='Update function'
    )
    update_parser.add_argument('target_dir', help='path to directory')

    args = parser.parse_args()
    command = args.command
    if not command:
        parser.print_help()
        return

    if command == 'function-update':
        update_function(args.target_dir)

if __name__ == '__main__':
    main()
