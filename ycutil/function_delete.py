from json import loads as load_json
from .entities import FunctionInfo
from .config import Config
from .logger import logger
from .yc_runner import run_yc

def delete_function(dir_path: str) -> FunctionInfo:
    logger.info('# delete function #')
    cfg = Config.from_dir(dir_path)
    out, _ = run_yc('delete', '--name', cfg.name)
    return FunctionInfo.from_json(load_json(out))
