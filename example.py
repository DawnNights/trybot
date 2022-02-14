import trybot

@trybot.on_full('hello')
def hello(session:trybot.Session):
    session.send_msg('hello world')

@trybot.on_command('say', mustGiven='你想让我读什么')
def reread(session:trybot.Session):
    session.send_msg(session.matched)

