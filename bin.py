#!/usr/bin/env python3

import argparse
from function_create import create_function
from function_update import update_function
from function_invoke import invoke_function

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Yandex Cloud functions wrapper'
    )
    subparsers = parser.add_subparsers(dest='command')

    create_function_parser = subparsers.add_parser(
        name='function-create',
        description='Create function',
    )
    create_function_parser.add_argument('target_dir', help='path to directory')

    update_function_parser = subparsers.add_parser(
        name='function-update',
        description='Update function',
    )
    update_function_parser.add_argument('target_dir', help='path to directory')

    invoke_function_parser = subparsers.add_parser(
        name='invoke-function',
        description='Invoke function',
    )
    invoke_function_parser.add_argument('target_dir', help='path to directory')

    args = parser.parse_args()
    command = args.command
    if not command:
        parser.print_help()
        return

    if command == 'function-create':
        create_function(args.target_dir)
    if command == 'function-update':
        update_function(args.target_dir)
    if command == 'function-invoke':
        invoke_function(args.target_dir)

if __name__ == '__main__':
    main()
