#!/usr/bin/env python3

import argparse
from function_create import create_function
from function_delete import delete_function
from function_update import update_function
from function_invoke import invoke_function
from function_list import list_functions
from function_logs import get_function_logs

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

    delete_function_parser = subparsers.add_parser(
        name='function-delete',
        description='Delete function',
    )
    delete_function_parser.add_argument('target_dir', help='path to directory')

    update_function_parser = subparsers.add_parser(
        name='function-update',
        description='Update function',
    )
    update_function_parser.add_argument('target_dir', help='path to directory')

    invoke_function_parser = subparsers.add_parser(
        name='function-invoke',
        description='Invoke function',
    )
    invoke_function_parser.add_argument('target_dir', help='path to directory')

    get_function_logs_parser = subparsers.add_parser(
        name='function-logs',
        description='Get function logs',
    )
    get_function_logs_parser.add_argument('target_dir', help='path to directory')

    subparsers.add_parser(
        name='function-list',
        description='List functions',
    )

    args = parser.parse_args()
    command = args.command
    if not command:
        parser.print_help()
        return

    if command == 'function-create':
        create_function(args.target_dir)
    if command == 'function-delete':
        delete_function(args.target_dir)
    if command == 'function-update':
        update_function(args.target_dir)
    if command == 'function-invoke':
        invoke_function(args.target_dir)
    if command == 'function-logs':
        get_function_logs(args.target_dir)
    if command == 'function-list':
        list_functions()

if __name__ == '__main__':
    main()
