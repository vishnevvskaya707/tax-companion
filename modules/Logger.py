import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

def setup_logger():
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s',
                                  datefmt='%d-%m-%y %H:%M:%S')

    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_handler.setFormatter(formatter)

    log_dir = './logs'
    os.makedirs(log_dir, exist_ok=True)

    f_handler = TimedRotatingFileHandler(filename=os.path.join(log_dir, 'bot.log'),
                                         when='W0',
                                         interval=1,
                                         backupCount=4,
                                         encoding='utf-8')
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(formatter)
    f_handler.suffix = '%Y-%m-%d'

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

logger = setup_logger()
logger.info('Logger is successfully configured with weekly rotation')