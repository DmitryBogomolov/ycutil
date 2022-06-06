from typing import Any, Tuple
from test_util import BaseTests, make_yc_mock, make_yc_call
from datetime import datetime
from ycfunc import (
    FunctionInfo,
    create_function, delete_function, get_function_info, list_functions,
)
from ycfunc.util import DATE_FORMAT

def make_test_pair(id: str, name: str, date: datetime) -> Tuple[Any, FunctionInfo]:
    raw = {
        'id': id,
        'name': name,
        'created_at': date.strftime(DATE_FORMAT),
        'status': 'OK',
        'http_invoke_url': f'http://{id}',
        'log_group_id': f'{id}-log',
    }
    info = FunctionInfo(id, name, date, 'OK', f'http://{id}', f'{id}-log')
    return (raw, info)

class CommonTests(BaseTests):
    def test_create_function(self) -> None:
        raw, info = make_test_pair('test-id', 'test-name', datetime(2000, 1, 2))
        self.run_mock.return_value = make_yc_mock(raw)

        ret = create_function(self.cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('create --name test-function'),
        )
        self.assertEqual(ret, info)

    def test_delete_function(self) -> None:
        raw, info = make_test_pair('test-id', 'test-name', datetime(2000, 2, 3))
        self.run_mock.return_value = make_yc_mock(raw)

        ret = delete_function(self.cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('delete --name test-function'),
        )
        self.assertEqual(ret, info)

    def test_get_function_info(self) -> None:
        raw, info = make_test_pair('test-id', 'test-name', datetime(2000, 3, 4))
        self.run_mock.return_value = make_yc_mock(raw)

        ret = get_function_info(self.cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('get --name test-function'),
        )
        self.assertEqual(ret, info)

    def test_list_functions(self) -> None:
        raw1, info1 = make_test_pair('test-id-1', 'test-name-1', datetime(2000, 4, 5))
        raw2, info2 = make_test_pair('test-id-2', 'test-name-2', datetime(2000, 5, 6))
        self.run_mock.return_value = make_yc_mock([raw1, raw2])

        ret = list_functions()

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('list'),
        )
        self.assertEqual(ret, [info1, info2])
