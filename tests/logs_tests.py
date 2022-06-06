from typing import Any, Dict, List, cast
from datetime import datetime
from test_util import BaseTests, make_yc_mock, make_yc_call
from ycfunc import (
    Config, FunctionLog,
    get_function_logs,
)
from ycfunc.util import DATE_FORMAT

def make_raw_log(request_id: str, **kwargs: Dict[str, Any]) -> Any:
    obj = {
        'json_payload': {'request_id': request_id},
    }
    if kwargs.get('is_start'):
        obj['level'] = 'INFO'
        obj['message'] = f'START RequestID: {request_id}'
        obj['timestamp'] = cast(datetime, kwargs['timestamp']).strftime(DATE_FORMAT)
    elif kwargs.get('is_end'):
        obj['level'] = 'INFO'
        obj['message'] = f'END RequestID: {request_id}'
        obj['timestamp'] = cast(datetime, kwargs['timestamp']).strftime(DATE_FORMAT)
    elif kwargs.get('is_report'):
        obj['level'] = 'INFO'
        obj['timestamp'] = datetime(1900, 1, 1).strftime(DATE_FORMAT)
        items = [
            f'REPORT RequestID: {request_id}',
            'Duration: 0.5 ms',
            'Billed Duration: 2 ms',
            'Memory Size: 12 MB',
            'Max Memory Used: 32 MB',
            'Queuing Duration: 5 ms',
        ]
        obj['message'] = ' '.join(items)
    else:
        obj['timestamp'] = datetime(1900, 1, 1).strftime(DATE_FORMAT)
        obj['message'] = kwargs['message']
    return obj

def make_log(request_id: str, messages: List[str], start: datetime, end: datetime) -> FunctionLog:
    return FunctionLog(request_id, messages, start, end, 0.5, 2.0, 12, 32, 5.0, 0.0)

class LogsTests(BaseTests):
    def test_get_function_logs(self) -> None:
        self.run_mock.return_value = make_yc_mock([
            make_raw_log('id-1', is_start=True, timestamp=datetime(2000, 1, 11)),
            make_raw_log('id-1', is_end=True, timestamp=datetime(2000, 1, 12)),
            make_raw_log('id-1', is_report=True),
        ])
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        ret = get_function_logs(cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('logs --name test-function'),
        )
        self.assertEqual(
            ret,
            [
                make_log('id-1', [], datetime(2000, 1, 11), datetime(2000, 1, 12)),
            ],
        )

    def test_get_function_logs_messages(self) -> None:
        self.run_mock.return_value = make_yc_mock([
            make_raw_log('id-1', is_start=True, timestamp=datetime(2000, 1, 11)),
            make_raw_log('id-1', message='Hello'),
            make_raw_log('id-1', is_end=True, timestamp=datetime(2000, 1, 12)),
            make_raw_log('id-1', message='World'),
            make_raw_log('id-1', is_report=True),
        ])
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        ret = get_function_logs(cfg)

        self.assertEqual(
            ret,
            [
                make_log('id-1', ['Hello', 'World'], datetime(2000, 1, 11), datetime(2000, 1, 12)),
            ],
        )

    def test_get_function_logs_several(self) -> None:
        self.run_mock.return_value = make_yc_mock([
            make_raw_log('id-1', is_start=True, timestamp=datetime(2000, 1, 23)),
            make_raw_log('id-1', is_end=True, timestamp=datetime(2000, 1, 24)),
            make_raw_log('id-1', is_report=True),
            make_raw_log('id-2', is_start=True, timestamp=datetime(2000, 1, 11)),
            make_raw_log('id-2', message='Hello'),
            make_raw_log('id-2', is_end=True, timestamp=datetime(2000, 1, 12)),
            make_raw_log('id-2', message='World'),
            make_raw_log('id-2', is_report=True),
        ])
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        ret = get_function_logs(cfg)

        self.assertEqual(
            ret,
            [
                make_log('id-1', [], datetime(2000, 1, 23), datetime(2000, 1, 24)),
                make_log('id-2', ['Hello', 'World'], datetime(2000, 1, 11), datetime(2000, 1, 12)),
            ],
        )
