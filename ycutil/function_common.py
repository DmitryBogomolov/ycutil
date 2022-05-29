from typing import List, Dict, Any, cast
from .entities import FunctionInfo
from .config import Config
from .logger import logger
from .yc_runner import run_yc

def create_function(dir_path: str) -> FunctionInfo:
    logger.info('# create_function #')
    cfg = Config.from_dir(dir_path)
    out = run_yc('create', '--name', cfg.name)
    return FunctionInfo.from_json(out)

def delete_function(dir_path: str) -> FunctionInfo:
    logger.info('# delete function #')
    cfg = Config.from_dir(dir_path)
    out = run_yc('delete', '--name', cfg.name)
    return FunctionInfo.from_json(out)

def get_function_info(dir_path: str) -> FunctionInfo:
    logger.info('# get function info #')
    cfg = Config.from_dir(dir_path)
    out = run_yc('get', '--name', cfg.name)
    return FunctionInfo.from_json(out)

def list_functions() -> List[FunctionInfo]:
    logger.info('# list functions #')
    out = run_yc('list')
    data_items = cast(List[Any], out)
    return [FunctionInfo.from_json(data_item) for data_item in data_items]

def get_function_logs(dir_path: str) -> List[Dict[str, Any]]:
    logger.info('# get function logs #')
    cfg = Config.from_dir(dir_path)
    return run_yc('logs', '--name', cfg.name)
