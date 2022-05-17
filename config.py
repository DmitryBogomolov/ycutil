from typing import NamedTuple
from os import path
import json

CONFIG_NAME = '.ycconf'

class Config(NamedTuple):
    root_dir: str
    name: str
    entrypoint: str
    timeout: int = 10
    memory: int = 128
    runtime: str = 'python37'

def read_config(dir_path: str) -> Config:
    file_path = path.join(path.abspath(dir_path), CONFIG_NAME)
    with open(file_path, encoding='utf8') as file_obj:
        content = json.load(file_obj)
    return Config(root_dir=path.abspath(dir_path), **content)
