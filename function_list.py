import re
from typing import List, Dict, Any, cast
from json import loads as load_json
from function_info import FunctionInfo
from logger import logger
from yc_runner import run_yc
from helper import parse_date

def list_functions() -> List[FunctionInfo]:
    logger.info('# list functions #')
    out, _ = run_yc(['list', '--format', 'json'])
    data_items = cast(List[Dict[str, Any]], load_json(out))
    function_list: List[FunctionInfo] = []
    for data_item in data_items:
        if data_item['status'] == 'ACTIVE':
            function_item = FunctionInfo(
                id = data_item['id'],
                name = data_item['name'],
                created_at = parse_date(data_item['created_at'])
            )
            function_list.append(function_item)
    return function_list

