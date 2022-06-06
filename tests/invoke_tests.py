from typing import Any
from test_util import BaseTests, make_yc_mock, make_yc_call
from datetime import datetime
from ycfunc import (
    Config,
    invoke_function,
)
from ycfunc.util import DATE_FORMAT

TEST_DATE = datetime(2000, 1, 2)
TEST_DATE_STR = TEST_DATE.strftime(DATE_FORMAT)

class InvokeTests(BaseTests):
    def test_invoke(self):
        self.run_mock.return_value = make_yc_mock(0)
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        ret = invoke_function(cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('invoke --name test-function'),
        )
        self.assertEqual(ret, 0)

    def test_invoke_with_data(self):
        self.run_mock.return_value = make_yc_mock(0)
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        ret = invoke_function(cfg, 'test-data')

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('invoke --name test-function --data test-data'),
        )
        self.assertEqual(ret, 0)

    def check_unpack_result(self, yc_ret: Any, expected_ret: Any, desc: str) -> None:
        self.run_mock.reset_mock()
        self.run_mock.return_value = make_yc_mock(yc_ret)
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        ret = invoke_function(cfg)

        self.assertEqual(ret, expected_ret, desc)

    def test_unpack_result(self) -> None:
        self.check_unpack_result(None, None, 'None')
        self.check_unpack_result(100, 100, 'int')
        self.check_unpack_result(1.2, 1.2, 'float')
        self.check_unpack_result(True, True, 'bool')
        self.check_unpack_result('test', 'test', 'str')
        self.check_unpack_result([1, 2, 3], [1, 2, 3], 'list')
        self.check_unpack_result({'a': 1}, {'a': 1}, 'dict')

    def check_pack_data(self, data: Any, expected_yc_arg: Any, desc: str) -> None:
        self.run_mock.reset_mock()
        self.run_mock.return_value = make_yc_mock(0)
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        invoke_function(cfg, data)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call(['invoke', '--name', 'test-function', '--data', expected_yc_arg]),
            desc,
        )

    def test_pack_data(self) -> None:
        self.check_pack_data(100, '100', 'int')
        self.check_pack_data(1.2, '1.2', 'float')
        self.check_pack_data(True, 'True', 'bool')
        self.check_pack_data('test', 'test', 'str')
        self.check_pack_data([1, 2, 3], '[1, 2, 3]', 'list')
        self.check_pack_data({'a': 1}, '{"a": 1}', 'dict')
