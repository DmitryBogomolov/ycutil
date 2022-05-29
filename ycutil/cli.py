from typing import Callable, cast
from os import getcwd
from argparse import ArgumentParser
from .config import Config
from .function_common import (
    create_function,
    delete_function,
    get_function_info,
    get_function_logs,
    list_functions,
)
from .function_update import (
    update_function,
    get_function_versions,
)
from .function_invoke import (
    invoke_function,
)
from .function_url import (
    is_url_invoke,
    set_url_invoke,
)

command_descriptors = [
    ('function-create', create_function),
    ('function-delete', delete_function),
    ('function-list', list_functions),
    ('function-info', get_function_info),
    ('function-logs', get_function_logs),
    ('function-update', update_function),
    ('function-versions', get_function_versions),
    ('function-invoke', invoke_function),
    ('function-is-url-invoke', is_url_invoke),
    ('function-set-url-invoke', set_url_invoke),
]

def run_cli() -> None:
    parser = ArgumentParser(
        description='Yandex Cloud functions wrapper'
    )
    parser.add_argument('--target-dir', default=getcwd(), help='path to directory')
    subparsers = parser.add_subparsers(dest='command')

    cmd_to_func = {}

    for name, func in command_descriptors:
        subparsers.add_parser(
            name=name,
            description=func.__doc__,
        )
        cmd_to_func[name] = func

    args = parser.parse_args()
    func = cast(Callable[[Config], None], cmd_to_func.get(args.command))
    cfg = Config.from_dir(args.target_dir)
    func(cfg)   # type: ignore
