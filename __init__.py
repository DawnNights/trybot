"""
Created on February 13 at 11:26 2022

"""

import asyncio
import threading

from .plugin import *
from .logger import logger
from .session import Session
from .driver import BotDriver


default_driver: BotDriver = None


def event_printer(event: dict):
    if 'group_id' in event and event['post_type'] == 'message':
        name = event['sender']['card']
        logger.info(
            '收到群聊(%d)内 %s(%d) 消息: %s' %
            (
                event['group_id'],
                name if name else event['sender']['nickname'],
                event['user_id'],
                event['message']
            ))
    elif 'user_id' in event and event['post_type'] == 'message':
        logger.info(
            '收到私聊 %s(%d) 消息: %s',
            event['sender']['nickname'],
            event['user_id'],
            event['message']
        )
    else:
        logger.info("收到事件: " + event.__str__())


async def event_handler(event: dict):
    session = Session(event, default_driver)
    for plugin in PluginPool:
        ret = await plugin(session).start_handle()
        if ret and plugin.block:
            break   # 截断后续执行


def run_bot(host: str = '127.0.0.1', port: int = 6700):
    global default_driver
    default_driver = BotDriver(host, port)
    loop = asyncio.get_event_loop()
    threading.Thread(
        args=(loop, event_handler, event_printer),
        target=default_driver.listen
    ).start()

    loop.run_forever()


__all__ = [
    'Session',
    'BotDriver',
    'run_bot',
    'on_event',
    'on_full',
    'on_fulls',
    'on_command',
    'on_commands',
    'on_regex',
]
