from operator import imod
from typing import NamedTuple, Dict, Any
from datetime import datetime
from helper import parse_date

class FunctionInfo(NamedTuple):
    id: str
    name: str
    created_at: datetime
    status: str
    invoke_url: str

    @staticmethod
    def from_json(content: Dict[str, Any]) -> 'FunctionInfo':
        return FunctionInfo(
            id = content['id'],
            name = content['name'],
            created_at = parse_date(content['created_at']),
            status = content['status'],
            invoke_url = content['http_invoke_url'],
        )
