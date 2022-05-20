import re
from typing import NamedTuple, List, Dict, Any, cast
from datetime import datetime
from json import loads as load_json
from logger import logger
from yc_runner import run_yc
from helper import parse_date

class FunctionInfo(NamedTuple):
    id: str
    name: str
    created_at: datetime

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

