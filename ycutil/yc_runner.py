from typing import Any
from json import loads as load_json
from subprocess import CalledProcessError, run, PIPE
from .logger import logger

def run_yc(*args: str) -> Any:
    run_args = ['yc', 'serverless', 'function', *args, '--no-user-output', '--format', 'json']
    logger.info('yc.run')
    logger.info(run_args[2:])
    try:
        proc = run(run_args, check=True, encoding='utf8', stdout=PIPE, stderr=PIPE)
        logger.info('yc.out')
        logger.info(proc.stdout + proc.stderr)
        return load_json(proc.stdout)
    except CalledProcessError as err:
        logger.error('yc.err')
        logger.error(err.stderr + err.stdout)
        raise RuntimeError(err.stderr) from err
