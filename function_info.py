from typing import NamedTuple
from datetime import datetime

class FunctionInfo(NamedTuple):
    id: str
    name: str
    created_at: datetime
