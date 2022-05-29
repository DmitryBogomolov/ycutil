from typing import List
from .entities import FunctionInfo, FunctionLogEntry
from .config import Config
from .yc_runner import run_yc

def create_function(cfg: Config) -> FunctionInfo:
    out = run_yc('create', '--name', cfg.name)
    return FunctionInfo.from_json(out)

def delete_function(cfg: Config) -> FunctionInfo:
    out = run_yc('delete', '--name', cfg.name)
    return FunctionInfo.from_json(out)

def get_function_info(cfg: Config) -> FunctionInfo:
    out = run_yc('get', '--name', cfg.name)
    return FunctionInfo.from_json(out)

def list_functions() -> List[FunctionInfo]:
    out = run_yc('list')
    return [*map(FunctionInfo.from_json, out)]

def get_function_logs(cfg: Config) -> List[FunctionLogEntry]:
    out = run_yc('logs', '--name', cfg.name)
    return [*map(FunctionLogEntry.from_json, out)]
