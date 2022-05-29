from typing import Any
from .config import Config
from .yc_runner import run_yc
from .logger import logger

def invoke_function(dir_path: str) -> Any:
    logger.info('# invoke function #')
    cfg = Config.from_dir(dir_path)
    return run_yc('invoke', '--name', cfg.name)
