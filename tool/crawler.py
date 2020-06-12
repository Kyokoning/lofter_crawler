from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths
from lib.config import cfg
from lib.config import update_config
import argparse
from lib.user_pigeonhole import person_blog
from lib.logger import create_logger
from lib.user_pigeonhole import save_tag

def parse_args():
    parser = argparse.ArgumentParser(description='Train setting')

    parser.add_argument('--cfg',
                        help='configure file name',
                        required=True, type=str) # 命令行里包含config文件位置

    args = parser.parse_args()
    return args


if __name__=='__main__':
    args = parse_args()
    update_config(cfg, args)  # 从config文件更新配置

    logger, _ = create_logger(cfg)
    logger.info(cfg)

    save_tag(cfg)

