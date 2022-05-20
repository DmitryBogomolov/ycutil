from config import Config
from logger import logger
from yc_runner import run_yc

def create_function(dir_path: str) -> None:
    logger.info('# create_function #')
    cfg = Config.from_dir(dir_path)
    run_yc(['create', '--name', cfg.name])
