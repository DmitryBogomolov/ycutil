#!/usr/bin/env python3

import argparse
from ycutil import (
    Config,
    create_function,
    delete_function,
    update_function,
    invoke_function,
    get_function_info,
    list_functions,
    get_function_logs,
    is_url_invoke,
    set_url_invoke,
    get_function_versions,
)

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

    get_function_info_parser = subparsers.add_parser(
        name='function-info',
        description='Get function info',
    )
    get_function_info_parser.add_argument('target_dir', help='path to directory')

    get_function_logs_parser = subparsers.add_parser(
        name='function-logs',
        description='Get function logs',
    )
    get_function_logs_parser.add_argument('target_dir', help='path to directory')

    subparsers.add_parser(
        name='function-list',
        description='List functions',
    )

    url_invoke_parser = subparsers.add_parser(
        name='function-url-invoke',
        description='Manage function url invoke',
    )
    url_invoke_parser.add_argument('target_dir', help='path to directory')
    url_invoke_parser.add_argument('--mode', choices=('on', 'off'), help='turn on or off')

    list_function_versions_parser = subparsers.add_parser(
        name='function-versions',
        description='Get function versions',
    )
    list_function_versions_parser.add_argument('target_dir', help='path to directory')

    args = parser.parse_args()
    command = args.command
    if not command:
        parser.print_help()
        return

    if command == 'function-create':
        create_function(Config.from_dir(args.target_dir))
    if command == 'function-delete':
        delete_function(Config.from_dir(args.target_dir))
    if command == 'function-update':
        update_function(Config.from_dir(args.target_dir))
    if command == 'function-invoke':
        invoke_function(Config.from_dir(args.target_dir))
    if command == 'function-info':
        get_function_info(Config.from_dir(args.target_dir))
    if command == 'function-logs':
        get_function_logs(Config.from_dir(args.target_dir))
    if command == 'function-list':
        list_functions()
    if command == 'function-versions':
        get_function_versions(Config.from_dir(args.target_dir))
    if command == 'function-url-invoke':
        if args.mode:
            set_url_invoke(Config.from_dir(args.target_dir), args.mode == 'on')
        else:
            is_url_invoke(Config.from_dir(args.target_dir))


if __name__ == '__main__':
    main()
