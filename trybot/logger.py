"""
此模块提供 trybot 日志的输出
"""
import sys
import logging


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    datefmt="%Y/%m/%d-%H:%M:%S",
    format='[%(name)s %(asctime)s] %(levelname)s: %(message)s'
)

logger = logging.getLogger('Trybot')

__all__ = ['logger']