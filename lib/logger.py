import logging
import time
import os
def create_logger(cfg):
    time_str = str(time.strftime('%Y-%m-%d-%H-%M'))
    if cfg.TYPE=='tag':
        log_file_name = '{}_{}.log'.format(cfg.TAG, time_str)
    elif cfg.TYPE == 'USER':
        log_file_name = 'USER_{}_{}.log'.format(cfg.USER, time_str)
    elif cfg.TYPE == 'USER_LIKE':
        log_file_name = 'USER_LIKE_{}_{}.log'.format(cfg.USER, time_str)

    if not os.path.exists(cfg.OUTPUT_DIR):
        os.makedirs(cfg.OUTPUT_DIR)
    log_file_path = os.path.join(cfg.OUTPUT_DIR, log_file_name)
    head = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename = log_file_path,
                        format = head)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    logging.getLogger('').addHandler(console)

    return logger, log_file_path