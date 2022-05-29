from .config import Config
from .logger import logger
from .yc_runner import run_yc

def is_url_invoke(dir_path: str) -> bool:
    logger.info('# is url invoke #')
    cfg = Config.from_dir(dir_path)
    out = run_yc('list-access-bindings', '--name', cfg.name)
    return TARGET_BINDING in out

TARGET_BINDING = {
    'role_id': 'serverless.functions.invoker',
    'subject': {
        'id': 'allUsers',
        'type': 'system',
    },
}

def set_url_invoke(dir_path: str, state: bool) -> None:
    logger.info('# set url invoke #')
    cfg = Config.from_dir(dir_path)
    action = ('allow' if state else 'deny') + '-unauthenticated-invoke'
    run_yc(action, '--name', cfg.name)
