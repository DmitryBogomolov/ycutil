from json import loads as load_json
from .entities import FunctionInfo
from .config import Config
from .logger import logger
from .yc_runner import run_yc

def get_function_data(dir_path: str) -> FunctionInfo:
    logger.info('# function data #')
    cfg = Config.from_dir(dir_path)
    out, _ = run_yc(['get', '--name', cfg.name, '--format', 'json'])
    return FunctionInfo.from_json(load_json(out))
