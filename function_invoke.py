from config import Config
from subprocess import run

def invoke_function(dir_path: str) -> None:
    cfg = Config.from_dir(dir_path)
    call_yc(cfg)

def call_yc(cfg: Config) -> None:
    args = [
        'yc', 'serverless', 'function', 'invoke',
        '--name', cfg.name,
    ]
    run(args, check=True)
