"""
此模块提供与 OneBot 的正向 websocket 通信
"""

import sys
import json
import queue
import socket
import asyncio
from .logger import logger
from typing import Dict, Generator


class Waiter(dict):
    async def wait(self, uid:int, ret:Generator):
        self[uid] = ret
        for _ in range(60):
            if not uid in self:
                return False
            await asyncio.sleep(0.5)
        logger.error(f'等待会话输入[{uid}] -> 超时......')
        return True


class BotDriver:
    def __init__(self, host: str, port: int) -> None:
        # 建立Tcp Socket连接
        self.__sock = socket.socket()
        self.__sock.connect((host, port))

        # 发送Websocket握手请求
        self.__sock.send(b'\n'.join([
            b'GET /ws HTTP/1.1',
            b'Host: 127.0.0.1:6700',
            b'Connection: Upgrade',
            b'Upgrade: websocket',
            b'Sec-WebSocket-Version: 13',
            b'Sec-WebSocket-Key: Bt4+Nfq12qxyxHslV2iFFg==\n\n'
        ]))

        # 判断Websocket Client是否创建成功
        ret = self.__sock.recv(1024)
        if not b'Sec-WebSocket-Accept' in ret:
            logger.warning(f'发出 WebSocket 连接: {host}:{port} -> 失败')
            sys.exit("ERROR: " + ret.__str__()[2:-1])
        logger.info(f'发出 WebSocket 连接: {host}:{port} -> 成功')

    def _send(self, data: bytes) -> None:
        # FIN(1 bit): 表示该消息是否结束
        # RSV(3*1 bit): 除扩展协议外一般为0值
        # OPCODE(4 bit): 表数据类型
        # Mask（1 bit): 表示是否需要进行掩码计算
        # Payload length(7/7+16/7+64 bits): 大小视数据长度而定
        # Masking-key(0 bit/4 bytes): 一个4 bytes大小用于掩码计算的key
        head = 1 << 15  # 0b1000000000000000
        head = head | (1 << 8)  # OPCODE_TEXT 文本数据
        head = head | (1 << 7)  # 此处代表需要掩码计算

        # 判断 Payload length
        dataLen = len(data)
        if dataLen < 126:
            head = (head | dataLen).to_bytes(2, 'big')
        else:
            head = (head | 126) if dataLen < 65536 else (head | 127)
            head = head.to_bytes(2, 'big') + dataLen.to_bytes(2, 'big')

        # 进行掩码计算
        head += bytes([63] * 4)  # Masking-key
        data = bytes([b ^ 63 for b in data])  # 相同byte进行计算比较方便

        self.__sock.send(head + data)

    def _recv(self) -> bytes:
        # go-cqhttp传输的websocket数据包格式均为OPCODE_TEXT
        # go-cqhttp传输的websocket数据包是没有进行掩码计算的
        data = self.__sock.recv(1024 * 8)
        data = data[2:] if len(data) < 126 else data[4:]
        return data

    def send(self, body: dict):
        data = json.dumps(body)
        self._send(data.encode())

    def recv(self) -> dict:
        data = self._recv()
        return json.loads(data)

    def listen(self, main_loop, event_handler, event_printer=print):
        self.backer = queue.Queue(maxsize=20)
        self.waiter: Dict[int, Generator] = Waiter()

        while True:
            event = self.recv()
            if 'echo' in event:  # API调用返回
                self.backer.put(event)
            elif 'meta_event_type' in event:  # 忽略心跳事件
                continue
            elif event.get('user_id', 0) in self.waiter:    # 会话等待
                event_printer(event)
                ret = self.waiter[event['user_id']]
                ret.send(event['message'])
                del self.waiter[event['user_id']]
            else:   # 调用event_handle处理事件
                event_printer(event)
                asyncio.run_coroutine_threadsafe(
                    loop=main_loop,
                    coro=event_handler(event)
                )


__all__ = ['BotDriver']
