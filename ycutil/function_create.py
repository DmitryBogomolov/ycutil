from json import loads as load_json
from .entities import FunctionInfo
from .config import Config
from .logger import logger
from .yc_runner import run_yc

def create_function(dir_path: str) -> FunctionInfo:
    logger.info('# create_function #')
    cfg = Config.from_dir(dir_path)
    out, _ = run_yc(['create', '--name', cfg.name, '--no-user-output', '--format', 'json'])
    return FunctionInfo.from_json(load_json(out))
