from typing import List, Tuple
from subprocess import CalledProcessError, run, PIPE

def run_yc(args: List[str]) -> Tuple[str, str]:
    run_args = ['yc', 'serverless', 'function', *args]
    try:
        proc = run(run_args, check=True, encoding='utf8', stdout=PIPE, stderr=PIPE)
        return (proc.stdout, proc.stderr)
    except CalledProcessError as e:
        message = e.stderr + e.stdout
        raise RuntimeError(message)
