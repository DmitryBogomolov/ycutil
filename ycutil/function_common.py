from typing import NamedTuple, List
from datetime import datetime
from collections import OrderedDict
from .config import Config
from .util import RawInfo, parse_date, stringify_date
from .yc_runner import run_yc

class FunctionInfo(NamedTuple):
    id: str
    name: str
    created_at: datetime
    status: str
    invoke_url: str
    log_group_id: str

    def dump(self) -> RawInfo:
        return OrderedDict(
            id=self.id,
            name=self.name,
            created_at=stringify_date(self.created_at),
            status=self.status,
            invoke_url=self.invoke_url,
            log_group_id=self.log_group_id,
        )

    @classmethod
    def parse(cls, content: RawInfo) -> 'FunctionInfo':
        return cls(
            id = content['id'],
            name = content['name'],
            created_at = parse_date(content['created_at']),
            status = content['status'],
            invoke_url = content['http_invoke_url'],
            log_group_id = content['log_group_id'],
        )

def create_function(cfg: Config) -> FunctionInfo:
    '''Create function'''
    out = run_yc('create', '--name', cfg.name)
    return FunctionInfo.parse(out)

def delete_function(cfg: Config) -> FunctionInfo:
    '''Delete function'''
    out = run_yc('delete', '--name', cfg.name)
    return FunctionInfo.parse(out)

def get_function_info(cfg: Config) -> FunctionInfo:
    '''Get function info'''
    out = run_yc('get', '--name', cfg.name)
    return FunctionInfo.parse(out)

def list_functions() -> List[FunctionInfo]:
    '''List functions'''
    out = run_yc('list')
    return [*map(FunctionInfo.parse, out)]
