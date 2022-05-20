from typing import List, Tuple
from subprocess import CalledProcessError, run, PIPE
from logger import logger

def run_yc(args: List[str]) -> Tuple[str, str]:
    run_args = ['yc', 'serverless', 'function', *args]
    logger.info('yc call: %s', ' '.join(run_args[2:]))
    try:
        proc = run(run_args, check=True, encoding='utf8', stdout=PIPE, stderr=PIPE)
        if proc.stdout:
            logger.info('yc out: %s', proc.stdout)
        if proc.stderr:
            logger.info('yc err: %s', proc.stderr)
        return (proc.stdout, proc.stderr)
    except CalledProcessError as err:
        if proc.stdout:
            logger.error('yc out: %s', proc.stdout)
        if proc.stderr:
            logger.error('yc err: %s', proc.stderr)
        message = err.stderr + err.stdout
        raise RuntimeError(message) from err
