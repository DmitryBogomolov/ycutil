from typing import List
from .entities import FunctionLogEntry
from .config import Config
from .yc_runner import run_yc

def get_function_logs(cfg: Config) -> List[FunctionLogEntry]:
    '''Get function logs'''
    out = run_yc('logs', '--name', cfg.name)
    return [*map(FunctionLogEntry.parse, out)]
