from typing import NamedTuple, Dict, Any
from datetime import datetime
from collections import OrderedDict

RawInfo = Dict[str, Any]

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, DATE_FORMAT)

def stringify_date(date: datetime) -> str:
    return date.strftime(DATE_FORMAT)

def dump_named_tuple(target: NamedTuple) -> OrderedDict:
    obj = OrderedDict()
    for name in target.__class__._fields:
        obj[name] = getattr(target, name)
        if target.__class__._field_types[name] == datetime:
            obj[name] = stringify_date(obj[name])
    return obj
