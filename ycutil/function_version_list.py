from typing import List, Any, cast
from json import loads as load_json
from .entities import FunctionVersionInfo
from .config import Config
from .logger import logger
from .yc_runner import run_yc

def list_function_versions(dir_path: str) -> List[FunctionVersionInfo]:
    logger.info('# list function versions #')
    cfg = Config.from_dir(dir_path)
    out, _ = run_yc(['version', 'list', '--function-name', cfg.name])
    data_items = cast(List[Any], load_json(out))
    return [FunctionVersionInfo.from_json(data_item) for data_item in data_items]
