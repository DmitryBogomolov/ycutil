from test_util import BaseTests, make_yc_mock, make_yc_call
from ycfunc import (
    Config, FunctionLog,
    get_function_logs,
)

class LogsTests(BaseTests):
    def test_get_function_logs(self) -> None:
        self.run_mock.return_value = make_yc_mock([
            
        ])
        cfg = Config('/test-dir', 'test-function', 'index.handler')

        ret = get_function_logs(cfg)

        self.assertEqual(
            self.run_mock.call_args,
            make_yc_call('logs --name test-function'),
        )
        self.assertEqual(
            ret,
            [],
        )

