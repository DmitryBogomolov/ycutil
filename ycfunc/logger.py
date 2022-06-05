from io import StringIO
from logging import getLogger, Formatter, StreamHandler, FileHandler, INFO

logger = getLogger('ycutil')
logger.setLevel(INFO)
formatter = Formatter('%(asctime)s %(name)s %(levelname)-8s %(message)s')

str_buffer = StringIO()
handler = StreamHandler(str_buffer)
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_log() -> str:
    return str_buffer.getvalue()

def set_file_log(file_path: str) -> None:
    handler = FileHandler(file_path, encoding='utf8')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
