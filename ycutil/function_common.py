from typing import List, Any, cast
from json import loads as load_json
from .entities import FunctionInfo
from .config import Config
from .logger import logger
from .yc_runner import run_yc

def create_function(dir_path: str) -> FunctionInfo:
    logger.info('# create_function #')
    cfg = Config.from_dir(dir_path)
    out, _ = run_yc('create', '--name', cfg.name)
    return FunctionInfo.from_json(load_json(out))

def delete_function(dir_path: str) -> FunctionInfo:
    logger.info('# delete function #')
    cfg = Config.from_dir(dir_path)
    out, _ = run_yc('delete', '--name', cfg.name)
    return FunctionInfo.from_json(load_json(out))

def get_function_info(dir_path: str) -> FunctionInfo:
    logger.info('# get function info #')
    cfg = Config.from_dir(dir_path)
    out, _ = run_yc('get', '--name', cfg.name)
    return FunctionInfo.from_json(load_json(out))

def list_functions() -> List[FunctionInfo]:
    logger.info('# list functions #')
    out, _ = run_yc('list')
    data_items = cast(List[Any], load_json(out))
    return [FunctionInfo.from_json(data_item) for data_item in data_items]

def get_function_logs(dir_path: str) -> str:
    logger.info('# get function logs #')
    cfg = Config.from_dir(dir_path)
    out, _ = run_yc('logs', '--name', cfg.name)
    return out
