from typing import Any, Dict, List, Tuple, Callable
from os import getcwd, path
from argparse import ArgumentParser, Namespace
from inspect import Signature, getdoc, signature
from json import dumps as dump_json
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
from .logger import set_file_log

CommandFunc = Callable[..., Any]

command_descriptors: List[Tuple[str, CommandFunc]] = [
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

def prettify_result(value: Any) -> Any:
    if not value:
        return value
    need_dump = False
    if hasattr(value, 'dump'):
        need_dump = True
        value = getattr(value, 'dump')()
    if isinstance(value, list):
        tmp = []
        for item in value:
            if hasattr(item, 'dump'):
                need_dump = True
                item = getattr(item, 'dump')()
            tmp.append(item)
        value = tmp
    if need_dump:
        return dump_json(value, indent=2)
    return value

def make_wrapper(func: CommandFunc, func_signature: Signature) -> Wrapper:
    def wrapper(parse_args: Namespace) -> None:
        func_args = {}
        target_dir = None
        for param_name, param_info in func_signature.parameters.items():
            if param_info.annotation == Config:
                target_dir = getattr(parse_args, 'target_dir')
                func_args[param_name] = Config.from_dir(target_dir)
            else:
                func_args[param_name] = getattr(parse_args, param_name)
        target_dir = target_dir or getcwd()
        set_file_log(path.join(target_dir, '.yclog'))
        func_ret = func(**func_args)
        func_ret = prettify_result(func_ret)
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
        func_signature = signature(func)
        for param_name, param_info in func_signature.parameters.items():
            if param_info.annotation == Config:
                subparser.add_argument('--target-dir', type=str, default=getcwd(), help='path to directory')
            else:
                subparser.add_argument('--' + param_name, required=True)

        cmd_to_func[name] = make_wrapper(func, func_signature)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    cmd_to_func[args.command](args)
