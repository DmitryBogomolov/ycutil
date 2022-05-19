from config import Config
from yc_runner import run_yc
from logger import logger

def invoke_function(dir_path: str) -> None:
    cfg = Config.from_dir(dir_path)
    logger.info('invoke_function')
    run_yc(['invoke', '--name', cfg.name])
