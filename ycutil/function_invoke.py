from typing import Any
from .config import Config
from .yc_runner import run_yc

# TODO: Provide args
def invoke_function(cfg: Config) -> Any:
    '''Invoke function'''
    return run_yc('invoke', '--name', cfg.name)
