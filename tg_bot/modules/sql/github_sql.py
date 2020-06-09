import threading

from sqlalchemy import Column, String, UnicodeText, Boolean, Integer, distinct, func

from tg_bot.modules.sql import BASE, SESSION


class GithubConfig(BASE):
    __tablename__ = "github_links"
    chat_id = Column(String(14), primary_key=True)
    repo = Column(String(100))

    def __init__(self, chat_id, repo=""):
        self.chat_id = chat_id
        self.repo = repo


def get_repo(chat_id):
    chat = SESSION.query(GithubConfig).filter(GithubConfig.chat_id == str(chat_id)).first()
    if not chat:
        return None
    return chat.repo


def register_repo(chat_id, repo):
    chat = SESSION.query(GithubConfig).filter(GithubConfig.chat_id == str(chat_id)).first()
    if not chat:
        chat = GithubConfig(chat_id, repo)
    else:
        chat.repo = repo
    SESSION.add(chat)
    SESSION.commit()
    return "Now tracking *%s*." % repo


def unregister_repo(chat_id):
    chat = SESSION.query(GithubConfig).filter(GithubConfig.chat_id == str(chat_id)).first()
    if not chat:
        return "This chat isn't tracking any repos!"
    repo = chat.repo
    SESSION.delete(chat)
    SESSION.commit()
    return "Stopped tracking *%s*." % repo
