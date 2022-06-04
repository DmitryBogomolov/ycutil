from typing import NamedTuple, List, Dict, Any, cast
from datetime import datetime
from itertools import groupby
from .config import Config
from .util import RawInfo, parse_date, dump_named_tuple
from .yc_runner import run_yc

class FunctionLog(NamedTuple):
    request_id: str
    messages: List[str]
    start_time: datetime
    end_time: datetime
    duration: float
    billed_duration: float
    memory_size: int
    max_memory_used: int
    queuing_duration: float
    function_init_duration: float = 0

    def dump(self) -> RawInfo:
        return dump_named_tuple(self)

def get_request_id(log_entry: Any) -> str:
    return log_entry['json_payload']['request_id']

def is_start_message(message: str, request_id: str) -> bool:
    return message.startswith(f'START RequestID: {request_id}')

def is_end_message(message: str, request_id: str) -> bool:
    return message.startswith(f'END RequestID: {request_id}')

def is_report_message(message: str, request_id: str) -> bool:
    return message.startswith(f'REPORT RequestID: {request_id}')

def extract_report_part(message: str, start: str, end: str) -> str:
    start_idx = message.index(start)
    end_idx = message.index(end, start_idx + len(start))
    return message[start_idx + len(start):end_idx]

def get_function_logs(cfg: Config) -> List[FunctionLog]:
    '''Get function logs'''
    out = run_yc('logs', '--name', cfg.name)
    logs = []
    for request_id, entries in groupby(out, key=get_request_id):
        args: Dict[str, Any] = {'request_id': request_id}
        messages = []
        for log_entry in entries:
            message = cast(str, log_entry['message'])
            if log_entry.get('level') == 'INFO':
                timestamp = parse_date(log_entry['timestamp'])
                if is_start_message(message, request_id):
                    args['start_time'] = timestamp
                elif is_end_message(message, request_id):
                    args['end_time'] = timestamp
                elif is_report_message(message, request_id):
                    args['duration'] = float(extract_report_part(message, 'Duration: ', ' ms'))
                    args['billed_duration'] = float(extract_report_part(message, 'Billed Duration: ', ' ms'))
                    args['memory_size'] = int(extract_report_part(message, 'Memory Size: ', ' MB'))
                    args['max_memory_used'] = int(extract_report_part(message, 'Max Memory Used: ', ' MB'))
                    args['queuing_duration'] = float(extract_report_part(message, 'Queuing Duration: ', ' ms'))
                    try:
                        args['function_init_duration'] = float(extract_report_part(message, 'Function Init Duration: ', ' ms'))
                    except:
                        pass
            else:
                messages.append(message)

        args['messages'] = messages
        logs.append(FunctionLog(**args))
    return logs
