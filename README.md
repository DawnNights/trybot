# TryBot
TryBot是一个基于 OneBot 标准，使用正向 WebSocket 通信的Python简易开发框架，且无第三方依赖，仅由 Python3 的标准库实现

# How to read code

### 实现 OneBot 通信

`driver.py` 封装了一个名为 BotDriver 的类用于进行正向 WebSocket 通信，它使用了标准库`socket`来创建底层的 TCP 连接，并按照实际需求编写了 WebSocket 数据包的实现代码

同时，定义一个 listen 方法用于循环接受事件，根据需求将其分成四种情况处理:

- API回调事件

当事件中含有`echo`字段是代表此事件为API回调事件，将其传入 self.backer 的队列中等待取出

- 心跳事件

存在`meta_event_type`字段的多是心跳事件，该事件类型无需处理，直接忽略

- 会话等待事件

当事件中`user_id`字段的值存在于 self.waiter 时，说明该用户的上一次会话正处于等待状态

取出对应的 generator 对象，通过 send 方法将事件消息传递给该会话调用

- 普通事件

对于非以上三种事件的普通事件，采用标准库 `asyncio` 来进行异步处理，通过 asyncio.run_coroutine_threadsafe 将异步事件处理函数 event_handler(event) 的协程任务加入传参中的事件循环 main_loop 中

### 封装 Session 调用

`session.py`中的 Session 类将部分常用的 OneBot Api 封装成了方法以便于用户调用，主要适配 [go-cqhttp](https://docs.go-cqhttp.org/)

### 编写 Plugin 功能

`plugin.py`内提供的装饰器函数使得用户可以轻松的创建一个 TryBot 的插件功能，例如:

```
import trybot

@trybot.on_full('复读', mustGiven='请输入复读的内容')
def reread(session: trybot.Session):
    session.send_msg(session.matched)

trybot.run_bot('127.0.0.1', 6700)
```

具体的代码可以在该文件中查看，主要是使用到了内置函数 type() 动态创建子类，以及生成器 generator 实现会话状态的操作