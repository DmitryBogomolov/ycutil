from typing import Any, Dict, List, Tuple, Callable
from os import getcwd, path
from argparse import ArgumentParser
from inspect import getdoc, getfullargspec
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
    invoke_function_url,
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
    ('function-invoke-url', invoke_function_url),
    ('function-is-url-invoke', is_url_invoke),
    ('function-set-url-invoke', set_url_invoke),
]

Wrapper = Callable[[Dict[str, Any]], None]

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

def make_wrapper(func: CommandFunc, config_arg: str) -> Wrapper:
    def wrapper(parse_args: Dict[str, Any]) -> None:
        target_dir = getcwd()
        if config_arg:
            target_dir = parse_args.pop('target_dir')
            parse_args[config_arg] = Config.from_dir(target_dir)
        set_file_log(path.join(target_dir, '.yclog'))
        func_ret = func(**parse_args)
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
        func_spec = getfullargspec(func)
        func_args = func_spec.args
        func_defaults = func_spec.defaults or tuple()
        first_default_idx = len(func_args) - len(func_defaults)
        has_config = len(func_args) > 0 and func_spec.annotations[func_args[0]] == Config
        if has_config:
            subparser.add_argument('--target-dir', type=str, default=getcwd(), help='path to directory')
        for arg_idx in range(int(has_config), len(func_args)):
            arg_name = func_args[arg_idx]
            if arg_idx < first_default_idx:
                subparser.add_argument('--' + arg_name, required=True)
            else:
                subparser.add_argument('--' + arg_name, default=func_defaults[arg_idx - first_default_idx])

        cmd_to_func[name] = make_wrapper(func, func_spec.args[0] if has_config else '')

    args = vars(parser.parse_args())
    cmd = args.pop('command')
    if not cmd:
        parser.print_help()
        return
    cmd_to_func[cmd](args)
