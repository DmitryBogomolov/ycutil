from typing import NamedTuple, Dict, Any
from datetime import datetime
from collections import OrderedDict

class FunctionInfo(NamedTuple):
    id: str
    name: str
    created_at: datetime
    status: str
    invoke_url: str
    log_group_id: str

    def to_json(self) -> OrderedDict:
        return OrderedDict(
            id=self.id,
            name=self.name,
            created_at=stringify_date(self.created_at),
            status=self.status,
            invoke_url=self.invoke_url,
            log_group_id=self.log_group_id,
        )

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
    status: str
    log_group_id: str
    entrypoint: str
    runtime: str
    memory: int
    timeout: int

    def to_json(self) -> OrderedDict:
        return OrderedDict(
            id=self.id,
            function_id=self.function_id,
            created_at=stringify_date(self.created_at),
            status=self.status,
            log_group_id=self.log_group_id,
            entrypoint=self.entrypoint,
            runtime=self.runtime,
            memory=self.memory,
            timeout=self.timeout,
        )

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

class FunctionLogEntry(NamedTuple):
    uid: str
    timestamp: datetime
    level: str
    message: str
    payload: Any

    def to_json(self) -> OrderedDict:
        return OrderedDict(
            uid=self.uid,
            timestamp=stringify_date(self.timestamp),
            level=self.level,
            message=self.message,
            payload=self.payload,
        )

    @classmethod
    def from_json(cls, content: Dict[str, Any]) -> 'FunctionLogEntry':
        return cls(
            uid = content['uid'],
            timestamp = parse_date(content['timestamp']),
            level = content['level'],
            message = content['message'],
            payload = content['json_payload'],
        )

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, DATE_FORMAT)

def stringify_date(date: datetime) -> str:
    return date.strftime(DATE_FORMAT)
