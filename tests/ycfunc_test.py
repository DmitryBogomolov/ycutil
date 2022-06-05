from unittest import TestCase
from unittest.mock import patch, Mock, call
from json import dumps
from datetime import datetime
from ycfunc import Config, FunctionInfo, get_function_info
from ycfunc.util import DATE_FORMAT

class TestYCFunc(TestCase):
    def setUp(self) -> None:
        run_patcher = patch('ycfunc.yc_runner.run')
        self.run_mock = run_patcher.start()
        self.addCleanup(run_patcher.stop)

    def test_get_function_info(self) -> None:
        ret = Mock(['stdout', 'stderr'])
        ret.stdout = dumps(dict(
            id='test-id',
            name='test-name',
            created_at=datetime(2000, 1, 2).strftime(DATE_FORMAT),
            status='OK',
            http_invoke_url='http://test',
            log_group_id='test-log-group',
        ))
        self.run_mock.return_value = ret
        cfg = Config('/test', 'test-function', 'index.handler')

        info = get_function_info(cfg)

        self.assertEqual(
            self.run_mock.call_args,
            call('yc serverless function get --name test-function --no-user-output --format json'.split(' '), check=True, encoding='utf8', stdout=-1, stderr=-1),
        )
        self.assertEqual(
            info,
            FunctionInfo('test-id', 'test-name', datetime(2000, 1, 2), 'OK', 'http://test', 'test-log-group'),
        )
