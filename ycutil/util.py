from typing import Dict, Any
from datetime import datetime

RawInfo = Dict[str, Any]

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, DATE_FORMAT)

def stringify_date(date: datetime) -> str:
    return date.strftime(DATE_FORMAT)
