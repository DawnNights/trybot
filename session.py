"""
此模块提供 OneBot Api 的封装
"""
from .logger import logger


class Session:
    def __init__(self, event, driver) -> None:
        self.event = event
        self.driver = driver
        self.matched = None

    def call_action(self, action: str, params: dict) -> dict:
        '''
        详情请查阅：https://docs.go-cqhttp.org/api/

        : param action: 调用Api的名称

        : param params: 提交给Api的参数

        '''
        self.driver.send({"action": action, "params": params, "echo": 123})
        logger.info(f"发送API[{action}]调用 <- {params}")
        try:    # 阻塞至响应或者等待30s超时
            return self.driver.backer.get(timeout=30)
        except:  # 等待30s超时异常捕获
            logger.error("接收API[{action}]返回 -> 超时......")

    def send_group_msg(self, group_id: int, message) -> int:
        '''

        发送群消息

        : param group_id: 群号

        : param message: 要发送的内容

        : return: 消息 ID

        '''
        params = {'group_id': group_id, "message": message}
        ret = self.call_action('send_group_msg', params)

        return 0 if ret is None or ret["status"] == "failed" else ret["data"]["message_id"]

    def send_private_msg(self, user_id: int, message) -> int:
        '''

        发送私聊消息

        : param user_id: 对方 QQ 号

        : param message: 要发送的内容

        : return: 消息 ID

        '''
        params = {'user_id': user_id, "message": message}
        ret = self.call_action('send_private_msg', params)

        return 0 if ret is None or ret["status"] == "failed" else ret["data"]["message_id"]

    def send_msg(self, message) -> int:
        '''

        快捷回复消息

        : param message: 要发送的内容

        : return: 消息 ID

        '''
        if self.event.get('group_id', 0):
            return self.send_group_msg(self.event['group_id'], message)
        else:
            return self.send_private_msg(self.event['user_id'], message)

    def send_group_forward_msg(self, group_id: int, messages) -> None:
        '''
        发送合并转发 ( 群 )

        : param group_id: 群号

        : param messages: List[trybot.message.customnode()]

        '''

        self.call_action(
            'send_group_forward_msg',
            {
                'group_id': group_id,
                'messages': messages
            }
        )

    def get_msg(self, message_id: int) -> dict:
        '''

        获取消息

        : param message_id: 消息id

        '''
        return self.call_action('get_msg', {'message_id': message_id})

    def delete_msg(self, message_id: int) -> None:
        '''

        撤回消息

        : param message_id: 消息id

        '''
        self.call_action('delete_msg', {'message_id': message_id})

    def set_group_kick(self, group_id: int, user_id: int, reject_add_request: bool = False) -> None:
        '''

        群组踢人

        : param group_id: 群号

        : param user_id: 要踢的 QQ 号

        : param reject_add_request: 拒绝此人的加群请求

        '''
        self.call_action(
            'set_group_kick',
            {
                "group_id": group_id,
                "user_id": user_id,
                "reject_add_request": reject_add_request
            }
        )

    def set_group_ban(self, group_id: int, user_id: int, duration: int = 30*60) -> None:
        '''

        群组单人禁言

        : param group_id: 群号

        : param user_id: 要禁言的 QQ 号

        : param duration: 禁言时长, 单位秒, 0 表示取消禁言

        '''
        self.call_action(
            'set_group_ban',
            {
                "group_id": group_id,
                "user_id": user_id,
                "duration": duration
            }
        )

    def set_group_whole_ban(self, group_id: int, enable: bool = True) -> None:
        '''

        群组全员禁言

        : param group_id: 群号

        : param enable: 是否禁言

        '''
        self.call_action(
            'set_group_whole_ban',
            {
                'group_id': group_id,
                "enable": enable
            }
        )

    def set_group_admin(self, group_id: int, user_id: int, enable: bool = True) -> None:
        '''

        群组设置管理员

        : param group_id: 群号

        : param user_id: 要设置管理员的 QQ 号

        : param enable: 是否禁言

        '''
        self.call_action(
            'set_group_admin',
            {
                "group_id": group_id,
                "user_id": user_id,
                "enable": enable
            }
        )

    def set_group_card(self, group_id: int, user_id: int, card: str = "") -> None:
        '''

        设置群名片 ( 群备注 )

        : param group_id: 群号

        : param user_id: 要设置的 QQ 号

        : param enable: 群名片内容, 不填或空字符串表示删除群名片

        '''
        self.call_action(
            'set_group_card',
            {
                "group_id": group_id,
                "user_id": user_id,
                "card": card
            }
        )

    def get_group_info(self, group_id: int, no_cache: bool = False) -> dict:
        '''

        获取群信息

        : param group_id: 群号

        : param no_cache: 是否不使用缓存(使用缓存可能更新不及时, 但响应更快)

        '''
        return self.call_action(
            'get_group_info',
            {
                'group_id': group_id, 'no_cache': no_cache
            }
        )

    def get_group_member_info(self, group_id: int, user_id: int, no_cache: bool = False) -> dict:
        '''

        获取群成员信息

        : param group_id: 群号

        : param user_id: QQ 号

        : param no_cache: 是否不使用缓存(使用缓存可能更新不及时, 但响应更快)

        '''
        return self.call_action(
            'get_group_member_info',
            {
                'group_id': group_id,
                'user_id': user_id,
                'no_cache': no_cache
            }
        )
