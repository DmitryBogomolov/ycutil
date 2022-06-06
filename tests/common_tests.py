from test_util import BaseTests, make_yc_mock, make_yc_call
from datetime import datetime
from ycfunc import (
    Config, FunctionInfo,
    create_function, delete_function, get_function_info, list_functions
)
from ycfunc.util import DATE_FORMAT

TEST_DATE = datetime(2000, 1, 2)
TEST_DATE_STR = TEST_DATE.strftime(DATE_FORMAT)

class CommonTests(BaseTests):
    def test_create_function(self) -> None:
        self.run_mock.return_value = make_yc_mock(dict(
            id='test-id',
            name='test-name',
            created_at=TEST_DATE_STR,
            status='OK',
            http_invoke_url='http://test',
            log_group_id='test-log-group',
        ))
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        info = create_function(cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('create --name test-function'),
        )
        self.assertEqual(
            info,
            FunctionInfo('test-id', 'test-name', TEST_DATE, 'OK', 'http://test', 'test-log-group'),
        )

    def test_delete_function(self) -> None:
        self.run_mock.return_value = make_yc_mock(dict(
            id='test-id',
            name='test-name',
            created_at=TEST_DATE_STR,
            status='OK',
            http_invoke_url='http://test',
            log_group_id='test-log-group',
        ))
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        info = delete_function(cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('delete --name test-function'),
        )
        self.assertEqual(
            info,
            FunctionInfo('test-id', 'test-name', TEST_DATE, 'OK', 'http://test', 'test-log-group'),
        )

    def test_get_function_info(self) -> None:
        self.run_mock.return_value = make_yc_mock(dict(
            id='test-id',
            name='test-name',
            created_at=TEST_DATE_STR,
            status='OK',
            http_invoke_url='http://test',
            log_group_id='test-log-group',
        ))
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        info = get_function_info(cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('get --name test-function'),
        )
        self.assertEqual(
            info,
            FunctionInfo('test-id', 'test-name', TEST_DATE, 'OK', 'http://test', 'test-log-group'),
        )

    def test_list_functions(self) -> None:
        self.run_mock.return_value = make_yc_mock([
            dict(
                id='test-id-1',
                name='test-name-1',
                created_at=TEST_DATE_STR,
                status='OK',
                http_invoke_url='http://test-1',
                log_group_id='test-log-group-1',
            ),
            dict(
                id='test-id-2',
                name='test-name-2',
                created_at=TEST_DATE_STR,
                status='OK',
                http_invoke_url='http://test-2',
                log_group_id='test-log-group-2',
            ),
        ])

        info = list_functions()

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('list'),
        )
        self.assertEqual(
            info,
            [
                FunctionInfo('test-id-1', 'test-name-1', TEST_DATE, 'OK', 'http://test-1', 'test-log-group-1'),
                FunctionInfo('test-id-2', 'test-name-2', TEST_DATE, 'OK', 'http://test-2', 'test-log-group-2'),
            ],
        )
