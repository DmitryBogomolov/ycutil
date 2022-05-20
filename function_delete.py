from typing import Dict, Any, cast
from json import loads as load_json
from function_info import FunctionInfo
from config import Config
from logger import logger
from helper import parse_date
from yc_runner import run_yc

def delete_function(dir_path) -> FunctionInfo:
    logger.info('# delete function #')
    cfg = Config.from_dir(dir_path)
    out, _ = run_yc(['delete', '--name', cfg.name, '--no-user-output', '--format', 'json'])
    data = cast(Dict[str, Any], load_json(out))
    return FunctionInfo(
        id = data['id'],
        name = data['name'],
        created_at = parse_date(data['created_at'])
    )

