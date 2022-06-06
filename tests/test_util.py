from typing import Any
from unittest import TestCase
from unittest.mock import Mock, _Call, patch, call, sentinel
from json import dumps

TEST_PIPE = sentinel.TEST_PIPE

def make_yc_mock(stdout: Any) -> Mock:
    ret = Mock(['stdout', 'stderr'])
    ret.stdout = dumps(stdout)
    return ret

def make_yc_call(cmd: str) -> _Call:
    return call(
        ('yc serverless function ' + cmd + ' --no-user-output --format json').split(' '),
        check=True, encoding='utf8', stdout=TEST_PIPE, stderr=TEST_PIPE
    )

class BaseTests(TestCase):
    def setUp(self) -> None:
        run_patcher = patch('ycfunc.yc_runner.run')
        pipe_patcher = patch('ycfunc.yc_runner.PIPE', new=TEST_PIPE)
        self.run_mock = run_patcher.start()
        pipe_patcher.start()
        self.addCleanup(run_patcher.stop)
        self.addCleanup(pipe_patcher.stop)
