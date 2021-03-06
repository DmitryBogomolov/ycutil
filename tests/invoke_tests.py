from typing import Any
from unittest.mock import Mock, patch, call
from datetime import datetime
from test_util import BaseTests, make_yc_mock, make_yc_call
from common_tests import make_test_pair
from ycfunc import (
    invoke_function, invoke_function_url, is_url_invoke, set_url_invoke,
)

class InvokeTests(BaseTests):
    def test_invoke(self):
        self.run_mock.return_value = make_yc_mock(0)

        ret = invoke_function(self.cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('invoke --name test-function'),
        )
        self.assertEqual(ret, 0)

    def test_invoke_with_data(self):
        self.run_mock.return_value = make_yc_mock(0)

        ret = invoke_function(self.cfg, 'test-data')

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('invoke --name test-function --data test-data'),
        )
        self.assertEqual(ret, 0)

    def check_unpack_result(self, yc_ret: Any, expected_ret: Any, desc: str) -> None:
        self.run_mock.reset_mock()
        self.run_mock.return_value = make_yc_mock(yc_ret)

        ret = invoke_function(self.cfg)

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

        invoke_function(self.cfg, data)

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

    @patch('ycfunc.invoke.post')
    def test_invoke_url(self, post_mock: Mock) -> None:
        raw, info = make_test_pair('test-id', 'test-name', datetime(2000, 1, 2))
        self.run_mock.return_value = make_yc_mock(raw)
        post_mock.return_value = Mock()
        post_mock.return_value.text = 'test-value'

        ret = invoke_function_url(self.cfg, 'test-data')

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('get --name test-function')
        )
        self.assertEqual(
            post_mock.call_args,
            call(info.http_invoke_url, data='test-data'),
        )
        self.assertEqual(ret, 'test-value')

    def test_is_url_invoke_false(self) -> None:
        self.run_mock.return_value = make_yc_mock([])

        ret = is_url_invoke(self.cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('list-access-bindings --name test-function'),
        )
        self.assertEqual(ret, False)

    def test_is_url_invoke_true(self) -> None:
        self.run_mock.return_value = make_yc_mock([
            {
                'role_id': 'serverless.functions.invoker',
                'subject': {
                    'id': 'allUsers',
                    'type': 'system',
                },
            }
        ])

        ret = is_url_invoke(self.cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('list-access-bindings --name test-function'),
        )
        self.assertEqual(ret, True)

    def test_set_url_invoke_false(self) -> None:
        self.run_mock.return_value = make_yc_mock(None)

        set_url_invoke(self.cfg, False)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('deny-unauthenticated-invoke --name test-function'),
        )

    def test_set_url_invoke_true(self) -> None:
        self.run_mock.return_value = make_yc_mock(None)

        set_url_invoke(self.cfg, True)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('allow-unauthenticated-invoke --name test-function'),
        )
