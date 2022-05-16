from typing import NamedTuple
from os import path
import json

CONFIG_NAME = '.ycconf'

class Config(NamedTuple):
    name: str
    entrypoint: str
    timeout: int = 10
    memory: int = 128
    runtime: str = 'python37'

def read_config(dir_path: str) -> Config:
    with open(path.join(dir_path, CONFIG_NAME), encoding='utf8') as file_obj:
        content = json.load(file_obj)
    return Config(**content)
