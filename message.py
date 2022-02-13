"""
此模块封装了适配 Go-cqhttp 的 OneBot 消息
"""

def text(text: str) -> dict:
    # https://docs.go-cqhttp.org/cqcode/#%E7%BA%AF%E6%96%87%E6%9C%AC
    return {"type": "text", "data": {"text": text}}


def face(id: int) -> dict:
    # https://docs.go-cqhttp.org/cqcode/#qq-%E8%A1%A8%E6%83%85
    return {"type": "face", "data": {"id": id}}


def record(file: str, cache=True) -> dict:
    # https://docs.go-cqhttp.org/cqcode/#%E8%AF%AD%E9%9F%B3
    return {"type": "record", "data": {"file": file, "cache": cache}}


def video(file: str, cover: str) -> dict:
    # https://docs.go-cqhttp.org/cqcode/#%E7%9F%AD%E8%A7%86%E9%A2%91
    return {"type": "video", "data": {"file": file, "cover": cover}}


def at(qq: int) -> dict:
    # https://docs.go-cqhttp.org/cqcode/#%E6%9F%90%E4%BA%BA
    return {"type": "at", "data": {"qq": qq}}


def share(url: str, title: str, content: str = '', image: str = '') -> dict:
    # https://docs.go-cqhttp.org/cqcode/#%E9%93%BE%E6%8E%A5%E5%88%86%E4%BA%AB
    return {"type": "share", "data": {"url": url, "title": title, 'content': content, 'image': image}}


def music(url: str, audio: str, title: str, content: str = '', image: str = '') -> dict:
    # https://docs.go-cqhttp.org/cqcode/#%E9%9F%B3%E4%B9%90%E8%87%AA%E5%AE%9A%E4%B9%89%E5%88%86%E4%BA%AB
    return {"type": "music", "data": {"type": "custom", "url": url, "audio": audio, "title": title, 'content': content, 'image': image}}


def image(file: str, cache=True) -> dict:
    # https://docs.go-cqhttp.org/cqcode/#%E5%9B%BE%E7%89%87
    return {"type": "image", "data": {"file": file, "cache": cache}}


def xml(data: str) -> dict:
    # https://docs.go-cqhttp.org/cqcode/#xml-%E6%B6%88%E6%81%AF
    return {"type": "xml", "data": {"data": data}}


def json(data: str) -> dict:
    # https://docs.go-cqhttp.org/cqcode/#json-%E6%B6%88%E6%81%AF
    return {"type": "json", "data": {"data": data}}


def cardimage(file: str) -> dict:
    # https://docs.go-cqhttp.org/cqcode/#cardimage
    return {"type": "cardimage", "data": {"file": file}}


def tts(text: str) -> dict:
    # https://docs.go-cqhttp.org/cqcode/#%E7%BA%AF%E6%96%87%E6%9C%AC
    return {"type": "tts", "data": {"text": text}}


def customnode(name: str, uin: int, content) -> dict:
    # https://docs.go-cqhttp.org/cqcode/#%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E6%B6%88%E6%81%AF%E8%8A%82%E7%82%B9
    return {"type": "node", "data": {"name": name, "uin": uin, "content": content}}
