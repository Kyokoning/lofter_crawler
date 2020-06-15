from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from yacs.config import CfgNode as CN

_C = CN()

_C.OUTPUT_DIR = ''
# tag模式'tag'/个人主页模式'USER'/个人喜欢模式'USER_LIKE'
_C.TYPE = 'tag'
# tag模式：保存目标tag中符合要求的blog
_C.TAG = []
# 个人主页模式：保存提供的个人主页中符合要求的blog
# 个人喜欢模式：保存提供的个人喜欢中符合要求的blog
_C.USER = []

# —— target：picture、article、热度多少以上、文章标题、tag(含有tag、不含有tag）
_C.TARGET = CN()
_C.TARGET.HOT_THRE = 0
_C.TARGET.TITLE = []
_C.TARGET.TAG_PLUS = []
_C.TARGET.TAG_MINUS = []

_C.EXTRA = CN()
# 存储的html需不需要加上发表时间
_C.EXTRA.TIME_STAMP = True

cfg = _C

def update_config(cfg, args):
    cfg.defrost()
    cfg.merge_from_file(args.cfg)
    cfg.freeze()

if __name__ == '__main__':
    print(_C)