from typing import Any
from base64 import b64encode
from .config import Config
from .yc_runner import run_yc

def invoke_function(cfg: Config, data: Any = None) -> Any:
    '''Invoke function'''
    args = ['invoke', '--name', cfg.name]
    if data is not None:
        args.append('--data')
        args.append(str(data))
    return run_yc(*args)
