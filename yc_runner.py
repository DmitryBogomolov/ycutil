from typing import List
from subprocess import run

def run_yc(args: List[str]) -> None:
    run_args = ['yc', 'serverless', 'function', *args]
    run(run_args, check=True)
