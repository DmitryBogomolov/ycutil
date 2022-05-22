from typing import NamedTuple, Dict, Any, cast
from os import path
from json import load as load_json
from .logger import logger

CONFIG_NAME = '.ycconf'
RUNTIMES = set(['python37', 'python38', 'python39'])
DEFAULT_TIMEOUT = 10
DEFAULT_MEMORY = 128
DEFAULT_RUNTIME = 'python37'

class Config(NamedTuple):
    root_dir: str
    name: str
    entrypoint: str
    timeout: int = DEFAULT_TIMEOUT
    memory: int = DEFAULT_MEMORY
    runtime: str = DEFAULT_RUNTIME

    @classmethod
    def from_dir(cls, dir_path: str) -> 'Config':
        root_dir = path.abspath(dir_path)
        file_path = path.join(root_dir, CONFIG_NAME)
        with open(file_path, encoding='utf8') as file_obj:
            content = cast(Dict[str, Any], load_json(file_obj))
        name = content.pop('name', '')
        if not name:
            raise ValueError('no "name" field')
        entrypoint = content.pop('entrypoint', '')
        if not entrypoint:
            raise ValueError('no "entrypoint" field')
        timeout = content.pop('timeout', DEFAULT_TIMEOUT)
        if not isinstance(timeout, int) or timeout < 1:
            raise ValueError(f'bad "timeout" field: {timeout}')
        memory = content.pop('memory', DEFAULT_MEMORY)
        if not isinstance(memory, int) or memory % 128 != 0 or memory < 128:
            raise ValueError(f'bad "memory" field: {memory}')
        runtime = content.pop('runtime', DEFAULT_RUNTIME)
        if runtime not in RUNTIMES:
            raise ValueError(f'bad "runtime" field: {runtime}')
        if len(content) > 0:
            fields = ', '.join(content.keys())
            raise ValueError(f'extra fields: {fields}')
        logger.info('directory: %s', root_dir)
        return cls(
            root_dir=root_dir,
            name=name,
            entrypoint=entrypoint,
            timeout=timeout,
            memory=memory,
            runtime=runtime,
        )
