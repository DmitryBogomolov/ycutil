from config import read_config, Config
from subprocess import run

def create_function(dir_path: str) -> None:
    cfg = read_config(dir_path)
    call_yc(cfg)

def call_yc(cfg: Config) -> None:
    args = [
        'yc', 'serverless', 'function', 'create',
        '--name', cfg.name,
    ]
    run(args, check=True)
