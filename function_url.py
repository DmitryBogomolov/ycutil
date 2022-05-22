from typing import List, Any, cast
from json import loads as load_json
from config import Config
from logger import logger
from yc_runner import run_yc

def is_url_invoke(dir_path: str) -> bool:
    logger.info('# is url invoke #')
    cfg = Config.from_dir(dir_path)
    out, _ = run_yc(['list-access-bindings', '--name', cfg.name, '--format', 'json'])
    bindings = cast(List[Any], load_json(out))
    return TARGET_BINDING in bindings

TARGET_BINDING = {
    'role_id': 'serverless.functions.invoker',
    'subject': {
        'id': 'allUsers',
        'type': 'system',
    },
}

def set_url_invoke(dir_path: str, state: bool) -> str:
    logger.info('# set url invoke #')
    cfg = Config.from_dir(dir_path)
    action = ('allow' if state else 'deny') + '-unauthenticated-invoke'
    out, _ = run_yc([action, '--name', cfg.name, '--no-user-output', '--format', 'json'])
    return out
