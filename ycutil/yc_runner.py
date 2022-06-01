from typing import Any
from json import loads as load_json
from subprocess import CalledProcessError, run, PIPE
from .logger import logger

def run_yc(*args: str) -> Any:
    run_args = ['yc', 'serverless', 'function', *args, '--no-user-output', '--format', 'json']
    logger.info('yc.run')
    logger.info(' '.join(run_args[2:]))
    try:
        proc = run(run_args, check=True, encoding='utf8', stdout=PIPE, stderr=PIPE)
        logger.info('yc.out')
        if proc.stdout:
            logger.info(proc.stdout)
        if proc.stderr:
            logger.info(proc.stderr)
        return load_json(proc.stdout) if proc.stdout else None
    except CalledProcessError as err:
        logger.error('yc.err')
        if err.stdout:
            logger.error(err.stdout)
        if err.stderr:
            logger.error(err.stderr)
        raise RuntimeError(err.stderr) from err
