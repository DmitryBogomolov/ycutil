from os import path
from json import load as load_json

CONFIG_NAME = '.ycconf'
RUNTIMES = set(['python37', 'python38', 'python39'])
DEFAULT_TIMEOUT = 10
DEFAULT_MEMORY = 128
DEFAULT_RUNTIME = 'python37'

class Config:
    root_dir: str
    name: str
    entrypoint: str
    timeout: int
    memory: int
    runtime: str

    def __init__(
        self,
        dir_path: str,
        name: str,
        entrypoint: str,
        timeout: int = DEFAULT_TIMEOUT,
        memory: int = DEFAULT_MEMORY,
        runtime: str = DEFAULT_RUNTIME,
    ):
        if not dir_path:
            raise ValueError(f'bad "dir_path": {dir_path}')
        if not name:
            raise ValueError(f'bad "name": {name}')
        if not entrypoint:
            raise ValueError(f'bad "entrypoint": {entrypoint}')
        if timeout < 1:
            raise ValueError(f'bad "timeout": {timeout}')
        if memory < 128 or memory % 128 != 0:
            raise ValueError(f'bad "memory": {memory}')
        if not runtime in RUNTIMES:
            raise ValueError(f'bad "runtime": {runtime}')
        self.root_dir = path.abspath(dir_path)
        self.name = name
        self.entrypoint = entrypoint
        self.timeout = timeout
        self.memory = memory
        self.runtime = runtime

    @classmethod
    def from_dir(cls, dir_path: str) -> 'Config':
        file_path = path.join(dir_path, CONFIG_NAME)
        with open(file_path, encoding='utf8') as file_obj:
            content = load_json(file_obj)
        return cls(dir_path=dir_path, **content)
