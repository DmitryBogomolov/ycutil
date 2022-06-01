from typing import Any
from requests import post
from .config import Config
from .yc_runner import run_yc

def invoke_function(cfg: Config, data: Any = None) -> Any:
    '''Invoke function'''
    args = ['invoke', '--name', cfg.name]
    if data is not None:
        args.append('--data')
        args.append(str(data))
    return run_yc(*args)

def invoke_function_url(cfg: Config, data: Any = None) -> Any:
    '''Invoke function by http request'''
    func_data = run_yc('get', '--name', cfg.name)
    func_url = func_data['http_invoke_url']
    response = post(func_url, data=data)
    return response.text
