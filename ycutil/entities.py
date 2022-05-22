from typing import NamedTuple, Dict, Any
from datetime import datetime
from .helper import parse_date

class FunctionInfo(NamedTuple):
    id: str
    name: str
    created_at: datetime
    status: str
    invoke_url: str
    log_group_id: str

    @classmethod
    def from_json(cls, content: Dict[str, Any]) -> 'FunctionInfo':
        return cls(
            id = content['id'],
            name = content['name'],
            created_at = parse_date(content['created_at']),
            status = content['status'],
            invoke_url = content['http_invoke_url'],
            log_group_id = content['log_group_id'],
        )

class FunctionVersionInfo(NamedTuple):
    id: str
    function_id: str
    created_at: datetime
    log_group_id: str
    status: str
    entrypoint: str
    runtime: str
    memory: int
    timeout: int

    @classmethod
    def from_json(cls, content: Dict[str, Any]) -> 'FunctionVersionInfo':
        return cls(
            id = content['id'],
            function_id = content['function_id'],
            created_at = parse_date(content['created_at']),
            log_group_id = content['log_group_id'],
            status = content['status'],
            entrypoint = content['entrypoint'],
            runtime = content['runtime'],
            memory = int(content['resources']['memory']) >> 20,
            timeout = int(content['execution_timeout'][:-1]),
        )
