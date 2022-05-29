from typing import Any
from .config import Config
from .yc_runner import run_yc

def invoke_function(cfg: Config) -> Any:
    return run_yc('invoke', '--name', cfg.name)
