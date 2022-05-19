from typing import NamedTuple, Dict, Any
from os import path, listdir
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from json import loads as load_json
from datetime import datetime
from config import Config
from yc_runner import run_yc

class UpdateInfo(NamedTuple):
    id: str
    created_at: datetime

def update_function(dir_path: str) -> UpdateInfo:
    cfg = Config.from_dir(dir_path)
    with TemporaryDirectory(dir=cfg.root_dir) as tmp_path:
        zip_path = path.join(tmp_path, cfg.name + '.zip')
        pack_code(zip_path, cfg.root_dir)
        status = call_yc(cfg, zip_path)
    return UpdateInfo(
        id = status['id'],
        created_at = datetime.strptime(status['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    )

def pack_code(zip_path: str, dir_path: str) -> None:
    with ZipFile(zip_path, mode='w') as zip_file:
        walk_code(dir_path, zip_file, dir_path)

def walk_code(root_path: str, zip_file: ZipFile, dir_path: str) -> None:
    for dir_item in listdir(dir_path):
        item_path = path.join(dir_path, dir_item)
        if path.isfile(item_path) and item_path.endswith('.py'):
            zip_file.write(item_path, path.relpath(item_path, root_path))
        elif path.isdir(item_path):
            walk_code(root_path, zip_file, item_path)

def call_yc(cfg: Config, zip_path: str) -> Dict[str, Any]:
    out, _ = run_yc([
        'version', 'create', '--no-user-output', '--format', 'json',
        '--function-name', cfg.name,
        '--entrypoint', cfg.entrypoint,
        '--runtime', cfg.runtime,
        '--memory', f'{cfg.memory}m',
        '--execution-timeout', f'{cfg.timeout}s',
        '--source-path', zip_path,
    ])
    return load_json(out)
