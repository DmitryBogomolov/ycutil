from typing import List, Any, cast
from json import loads as load_json
from .entities import FunctionInfo
from .logger import logger
from .yc_runner import run_yc

def list_functions() -> List[FunctionInfo]:
    logger.info('# list functions #')
    out, _ = run_yc(['list'])
    data_items = cast(List[Any], load_json(out))
    return [FunctionInfo.from_json(data_item) for data_item in data_items]
