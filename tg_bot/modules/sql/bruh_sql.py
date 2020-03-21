import threading

from sqlalchemy import Column, String, UnicodeText, Boolean, Integer, distinct, func

from tg_bot.modules.sql import BASE, SESSION


class BruhCount(BASE):
    __tablename__ = "bruh_count"
    chat_id = Column(String(14), primary_key=True)
    count = Column(Integer)

    def __init__(self, chat_id, count = 0):
        self.chat_id = chat_id
        self.count = count


def new_bruh_moment(chat_id):
    chat = SESSION.query(BruhCount).filter(BruhCount.chat_id == str(chat_id)).first()
    if chat:
        chat.count += int(1)
        SESSION.add(chat)
        SESSION.commit()
        return chat.count
    else:
        new_chat = BruhCount(
            chat_id = chat_id,
            count = 1
        )
        SESSION.add(new_chat)
        SESSION.commit()
        return 1