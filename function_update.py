from os import path, listdir
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from config import Config
from yc_runner import run_yc

def update_function(dir_path: str) -> None:
    cfg = Config.from_dir(dir_path)
    with TemporaryDirectory(dir=cfg.root_dir) as tmp_path:
        zip_path = path.join(tmp_path, cfg.name + '.zip')
        pack_code(zip_path, cfg.root_dir)
        call_yc(cfg, zip_path)

def pack_code(zip_path: str, dir_path: str) -> None:
    with ZipFile(zip_path, mode='w') as zip_file:
        walk_code(dir_path, zip_file, dir_path)
    return zip_path

def walk_code(root_path: str, zip_file: ZipFile, dir_path: str) -> None:
    for dir_item in listdir(dir_path):
        item_path = path.join(dir_path, dir_item)
        if path.isfile(item_path) and item_path.endswith('.py'):
            zip_file.write(item_path, path.relpath(item_path, root_path))
        elif path.isdir(item_path):
            walk_code(root_path, zip_file, item_path)

def call_yc(cfg: Config, zip_path: str) -> None:
    run_yc([
        'version', 'create',
        '--function-name', cfg.name,
        '--entrypoint', cfg.entrypoint,
        '--runtime', cfg.runtime,
        '--memory', f'{cfg.memory}m',
        '--execution-timeout', f'{cfg.timeout}s',
        '--source-path', zip_path,
    ])