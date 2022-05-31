from typing import Any, Dict, Callable
from os import getcwd
from argparse import ArgumentParser, Namespace
from inspect import Signature, getdoc, signature
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

Wrapper = Callable[[Namespace], None]

def make_wrapper(func: Any, func_signature: Signature) -> Wrapper:
    def wrapper(parse_args: Namespace) -> None:
        func_args = {}
        for param_name, param_info in func_signature.parameters.items():
            if param_info.annotation == Config:
                func_args[param_name] = Config.from_dir(getattr(parse_args, 'target_dir'))
            else:
                func_args[param_name] = getattr(parse_args, param_name)
        func_ret = func(**func_args)
        print(func_ret)

    return wrapper

def run_cli() -> None:
    parser = ArgumentParser(
        description='Yandex Cloud functions wrapper'
    )
    subparsers = parser.add_subparsers(dest='command')
    cmd_to_func: Dict[str, Wrapper] = {}

    for name, func in command_descriptors:
        subparser = subparsers.add_parser(
            name=name,
            description=getdoc(func),
        )
        func_signature = signature(func)    # type: ignore
        for param_name, param_info in func_signature.parameters.items():
            if param_info.annotation == Config:
                subparser.add_argument('--target-dir', type=str, default=getcwd(), help='path to directory')
            else:
                subparser.add_argument('--' + param_name, type=param_info.annotation, required=True)

        cmd_to_func[name] = make_wrapper(func, func_signature)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    cmd_to_func[args.command](args)