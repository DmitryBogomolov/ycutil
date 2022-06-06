from test_util import BaseTests, make_yc_mock, make_yc_call
from datetime import datetime
from ycfunc import Config, FunctionInfo, get_function_info
from ycfunc.util import DATE_FORMAT

class CommonTests(BaseTests):
    def test_get_function_info(self) -> None:
        ret = make_yc_mock(dict(
            id='test-id',
            name='test-name',
            created_at=datetime(2000, 1, 2).strftime(DATE_FORMAT),
            status='OK',
            http_invoke_url='http://test',
            log_group_id='test-log-group',
        ))
        self.run_mock.return_value = ret
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        info = get_function_info(cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('get --name test-function'),
        )
        self.assertEqual(
            info,
            FunctionInfo('test-id', 'test-name', datetime(2000, 1, 2), 'OK', 'http://test', 'test-log-group'),
        )
