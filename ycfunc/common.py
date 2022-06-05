import re
from typing import NamedTuple, List
from datetime import datetime
from .config import Config
from .util import RawInfo, parse_date, dump_named_tuple
from .yc_runner import run_yc

class FunctionInfo(NamedTuple):
    id: str
    name: str
    created_at: datetime
    status: str
    http_invoke_url: str
    log_group_id: str

    def dump(self) -> RawInfo:
        return dump_named_tuple(self)

    @classmethod
    def parse(cls, content: RawInfo) -> 'FunctionInfo':
        args = {}
        for name in cls._fields:
            args[name] = content[name]
            if cls._field_types[name] == datetime:
                args[name] = parse_date(args[name])
        return cls(**args)

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
