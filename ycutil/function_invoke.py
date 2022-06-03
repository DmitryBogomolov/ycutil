from typing import Any
from requests import post
from json import dumps as dump_json
from .config import Config
from .yc_runner import run_yc

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
