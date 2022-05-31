from typing import Dict, List, Any, cast
from os import path, listdir
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from .entities import FunctionVersionInfo
from .config import Config
from .logger import logger
from .yc_runner import run_yc

def update_function(cfg: Config) -> FunctionVersionInfo:
    '''Update function'''
    with TemporaryDirectory(dir=cfg.root_dir) as tmp_path:
        zip_path = path.join(tmp_path, cfg.name + '.zip')
        pack_code(zip_path, cfg.root_dir)
        out = run_yc(
            'version', 'create',
            '--function-name', cfg.name,
            '--entrypoint', cfg.entrypoint,
            '--runtime', cfg.runtime,
            '--memory', f'{cfg.memory}m',
            '--execution-timeout', f'{cfg.timeout}s',
            '--source-path', zip_path,
        )
    return FunctionVersionInfo.from_dict(cast(Dict[str, Any], out))

def pack_code(zip_path: str, dir_path: str) -> None:
    logger.info('collect files')
    with ZipFile(zip_path, mode='w') as zip_file:
        walk_code(dir_path, zip_file, dir_path)
    logger.info('archive: %s', zip_path)

def walk_code(root_path: str, zip_file: ZipFile, dir_path: str) -> None:
    for dir_item in listdir(dir_path):
        item_path = path.join(dir_path, dir_item)
        if path.isfile(item_path) and item_path.endswith('.py'):
            zip_file.write(item_path, path.relpath(item_path, root_path))
        elif path.isdir(item_path):
            walk_code(root_path, zip_file, item_path)

def get_function_versions(cfg: Config) -> List[FunctionVersionInfo]:
    '''Get function versions'''
    out = run_yc('version', 'list', '--function-name', cfg.name)
    data_items = cast(List[Any], out)
    return [FunctionVersionInfo.from_dict(data_item) for data_item in data_items]
