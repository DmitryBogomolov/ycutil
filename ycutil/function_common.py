from typing import List
from .entities import FunctionInfo, FunctionLogEntry
from .config import Config
from .yc_runner import run_yc

def create_function(cfg: Config) -> FunctionInfo:
    '''Create function'''
    out = run_yc('create', '--name', cfg.name)
    return FunctionInfo.parse(out)

def delete_function(cfg: Config) -> FunctionInfo:
    '''Delete function'''
    out = run_yc('delete', '--name', cfg.name)
    return FunctionInfo.parse(out)

def get_function_info(cfg: Config) -> FunctionInfo:
    '''Get function info'''
    out = run_yc('get', '--name', cfg.name)
    return FunctionInfo.parse(out)

def list_functions() -> List[FunctionInfo]:
    '''List functions'''
    out = run_yc('list')
    return [*map(FunctionInfo.parse, out)]

def get_function_logs(cfg: Config) -> List[FunctionLogEntry]:
    '''Get function logs'''
    out = run_yc('logs', '--name', cfg.name)
    return [*map(FunctionLogEntry.parse, out)]
