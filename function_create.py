from config import Config
from yc_runner import run_yc

def create_function(dir_path: str) -> None:
    cfg = Config.from_dir(dir_path)
    run_yc(['create', '--name', cfg.name])
