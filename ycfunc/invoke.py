from typing import Any
from requests import post
from json import dumps as dump_json
from .config import Config
from .yc_runner import run_yc

# Cloud function will try to guess type when data is provided in "event".
# true,false -> bool
# 1 -> int
# 1.2 -> float
# 'test' -> str
# [1, 'a'] -> list
# {'a': 1} -> dict
def pack_data(data: Any) -> str:
    if isinstance(data, str):
        return data
    if isinstance(data, (int, float)):
        return str(data)
    if isinstance(data, bool):
        return 'true' if data else 'false'
    return dump_json(data)

def invoke_function(cfg: Config, data: Any = None) -> Any:
    '''Invoke function'''
    args = ['invoke', '--name', cfg.name]
    if data is not None:
        args = [*args, '--data', pack_data(data)]
    return run_yc(*args)

def invoke_function_url(cfg: Config, data: Any = None) -> Any:
    '''Invoke function by http request'''
    func_data = run_yc('get', '--name', cfg.name)
    func_url = func_data['http_invoke_url']
    response = post(func_url, data=data)
    return response.text

def is_url_invoke(cfg: Config) -> bool:
    '''Get url invokation status'''
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
    '''Set url invokation status'''
    action = ('allow' if state else 'deny') + '-unauthenticated-invoke'
    run_yc(action, '--name', cfg.name)
