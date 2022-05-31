from io import StringIO
from logging import getLogger, Formatter, StreamHandler, INFO

logger = getLogger('ycutil')
str_buffer = StringIO()
handler = StreamHandler(str_buffer)
formatter = Formatter('%(asctime)s %(name)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.setLevel(INFO)
logger.addHandler(handler)

def get_log() -> str:
    return str_buffer.getvalue()
