from sys import stdout
from logging import getLogger, StreamHandler, INFO

logger = getLogger('ycutil')
handler = StreamHandler(stdout)
logger.setLevel(INFO)
logger.addHandler(handler)
