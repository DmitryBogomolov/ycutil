from .config import Config
from .yc_runner import run_yc

def is_url_invoke(cfg: Config) -> bool:
    out = run_yc('list-access-bindings', '--name', cfg.name)
    return TARGET_BINDING in out

TARGET_BINDING = {
    'role_id': 'serverless.functions.invoker',
    'subject': {
        'id': 'allUsers',
        'type': 'system',
    },
}

def set_url_invoke(cfg: Config, state: bool) -> None:
    action = ('allow' if state else 'deny') + '-unauthenticated-invoke'
    run_yc(action, '--name', cfg.name)
