from config import Config
from logger import logger
from yc_runner import run_yc

def delete_function(dir_path) -> None:
    logger.info('# delete function #')
    cfg = Config.from_dir(dir_path)
    run_yc(['delete', '--name', cfg.name, '--no-user-output', '--format', 'json'])
