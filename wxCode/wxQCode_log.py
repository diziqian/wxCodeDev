# coding:utf-8

import logging
from wxQCode_const import LOG_FILE

def initlog():
    l_logger = logging.getLogger()
    hdlr = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when='H', interval=1, backupCount=40)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    l_logger.addHandler(hdlr)
    l_logger.setLevel(logging.NOTSET)
    return l_logger


logger = initlog()