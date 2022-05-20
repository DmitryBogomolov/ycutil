from sys import stdout
from logging import getLogger, Formatter, StreamHandler, INFO

logger = getLogger('ycutil')
handler = StreamHandler(stdout)
formatter = Formatter('%(asctime)s %(name)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.setLevel(INFO)
logger.addHandler(handler)
