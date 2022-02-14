"""
此模块封装了 trybot 插件的编写功能
"""


from .logger import logger
from .session import Session
from re import findall
from typing import List, Callable, Generator


class Plugin:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def match(self) -> bool:
        for rule in self.rules:
            ret = rule(self.session)
            uid = next(ret)

            if uid is False:
                return False
            elif uid is True:
                continue
            elif await self.session.driver.waiter.wait(uid, ret):
                return False
        return True

    async def start_handle(self) -> bool:
        if await self.match():
            self.handle()
            return True
        return False


PluginPool: List[Plugin] = []


def on_event(*rules: Callable[[Session], Generator], priority: int = 10, block: bool = False):
    '''
    事件触发器

    : param rules: 事件匹配规则集

    : param priority: 插件优先级(数值越小级别越高)

    : param block: 当前插件处理成功后是否阻断后续插件执行
    '''
    def wrapper(func: Callable[[Session], None]):
        name = func.__name__.title()
        PluginPool.append(type(name, (Plugin, ), {
            'block': block,
            'rules': rules,
            'priority': priority,
            'handle': lambda p: func(p.session)
        }))
        PluginPool.sort(key=lambda p: p.priority)

        logger.info(f'插件[{name}]已导入，当前共计{len(PluginPool)}组插件')

    return wrapper


def on_full(keyword: str, *rules: Callable[[Session], Generator], mustGiven: str = '',  **kwargs):
    '''
    完全匹配触发器

    : param keyword: 匹配关键词

    : param rules: 事件匹配规则集

    : param mustGiven: 发送mustGiven语句并等待传参

    : param priority: 插件优先级(数值越小级别越高)

    : param block: 当前插件处理成功后是否阻断后续插件执行

    匹配结果保留至session.matched
    
    '''
    def full_rule(session: Session):
        if keyword == session.event['message']:
            if mustGiven:
                session.send_msg(mustGiven)
                session.matched = yield session.event['user_id']
            else:
                yield True
        yield False
    return on_event(*rules, full_rule, **kwargs)


def on_fulls(keywords: List[str], *rules: Callable[[Session], Generator], mustGiven: str = '',  **kwargs):
    '''
    完全匹配组触发器

    : param keywords: 匹配关键词组

    : param rules: 事件匹配规则集

    : param mustGiven: 发送mustGiven语句并等待传参

    : param priority: 插件优先级(数值越小级别越高)

    : param block: 当前插件处理成功后是否阻断后续插件执行

    匹配结果保留至session.matched
    
    '''
    def fulls_rule(session: Session):
        if session.event['message'] in keywords:
            if mustGiven:
                session.send_msg(mustGiven)
                session.matched = yield session.event['user_id']
            else:
                yield True
        yield False
    return on_event(*rules, fulls_rule, **kwargs)


def on_command(cmd: str, *rules: Callable[[Session], Generator], mustGiven: str = '',  **kwargs):
    '''
    命令匹配触发器

    : param cmd: 匹配命令

    : param rules: 事件匹配规则集

    : param mustGiven: 发送mustGiven语句并等待传参

    : param priority: 插件优先级(数值越小级别越高)

    : param block: 当前插件处理成功后是否阻断后续插件执行

    匹配结果保留至session.matched
    
    '''
    def cmd_rule(session: Session):
        if session.event['message'].startswith(cmd):
            session.matched = session.event['message'][len(cmd):].strip()
            if not session.matched and mustGiven:
                session.send_msg(mustGiven)
                session.matched = yield session.event['user_id']
            yield bool(session.matched)
        yield False
    return on_event(*rules, cmd_rule, **kwargs)


def on_commands(cmds: List[str], *rules: Callable[[Session], Generator], mustGiven: str = '',  **kwargs):
    '''
    命令组匹配触发器

    : param cmds: 匹配命令组

    : param rules: 事件匹配规则集

    : param mustGiven: 发送mustGiven语句并等待传参

    : param priority: 插件优先级(数值越小级别越高)

    : param block: 当前插件处理成功后是否阻断后续插件执行

    匹配结果保留至session.matched
    
    '''
    def cmds_rule(session: Session):
        for cmd in cmds:
            if session.event['message'].startswith(cmd):
                session.matched = session.event['message'][len(cmd):].strip()
                if not session.matched and mustGiven:
                    session.send_msg(mustGiven)
                    session.matched = yield session.event['user_id']
                yield bool(session.matched)
        yield False
    return on_event(*rules, cmds_rule, **kwargs)

def on_regex(pattern:str, *rules: Callable[[Session], Generator],  **kwargs):
    '''
    命令组匹配触发器

    : param pattern: 正则语句

    : param rules: 事件匹配规则集


    : param priority: 插件优先级(数值越小级别越高)

    : param block: 当前插件处理成功后是否阻断后续插件执行

    匹配结果保留至session.matched
    
    '''
    def reg_rule(session: Session):
        session.matched = findall(pattern, session.event['message'])
        yield bool(session.matched)
    
    return on_event(*rules, reg_rule, **kwargs)