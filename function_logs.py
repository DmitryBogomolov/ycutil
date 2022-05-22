#from json import loads as load_json
from config import Config
from logger import logger
from yc_runner import run_yc

def get_function_logs(dir_path: str) -> str:
    logger.info('# function logs #')
    cfg = Config.from_dir(dir_path)
    out, _ = run_yc(['logs', '--no-user-output', '--format', 'json', '--name', cfg.name])
    return out