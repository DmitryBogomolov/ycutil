from typing import Any, Tuple
from test_util import BaseTests, make_yc_mock, make_yc_call
from datetime import datetime
from ycfunc import (
    FunctionVersionInfo,
    get_function_versions,
)
from ycfunc.util import DATE_FORMAT

def make_test_pair(id: str, function_id: str, date: datetime) -> Tuple[Any, FunctionVersionInfo]:
    raw = {
        'id': id,
        'function_id': function_id,
        'created_at': date.strftime(DATE_FORMAT),
        'log_group_id': f'{id}-log',
        'status': 'OK',
        'entrypoint': 'index.handler',
        'runtime': 'runtime',
        'resources': {'memory': 16 << 20},
        'execution_timeout': '5s',
    }
    info = FunctionVersionInfo(id, function_id, date, 'OK', f'{id}-log', 'index.handler', 'runtime', 16, 5)
    return (raw, info)

class UpdateTests(BaseTests):
    def test_get_function_versions(self) -> None:
        raw1, info1 = make_test_pair('id-1', 'fid-1', datetime(2000, 1, 2))
        raw2, info2 = make_test_pair('id-2', 'fid-2', datetime(2000, 2, 3))
        self.run_mock.return_value = make_yc_mock([raw1, raw2])

        ret = get_function_versions(self.cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('version list --function-name test-function'),
        )
        self.assertEqual(ret, [info1, info2])
