from config import Config
from yc_runner import run_yc

def invoke_function(dir_path: str) -> None:
    cfg = Config.from_dir(dir_path)
    run_yc(['invoke', '--name', cfg.name])
