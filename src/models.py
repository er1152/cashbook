from datetime import datetime
from db import Base

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN

import hashlib

SQLITE3_NAME = "./db.sqlite3"


class Item(Base):
    """
    項目クラス
    id : id(主キー)
    date : 日付
    cost : 金額
    detail : 詳細
    category : カテゴリ
    is_in : 収入かどうか（収入->True,支出->False）
    """
    __tablename__ = "item"
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    date = Column("date", DateTime, default=datetime.now(),
                  nullable=False, server_default=current_timestamp())
    cost = Column("cost", INTEGER(unsigned=True), nullable=False,)
    detail = Column("detail", String(256))
    category = Column("category", String(256))
    is_in = Column("is_in", BOOLEAN, default=True, nullable=False)

    def __init__(self, date, cost, detail, category, is_in):
        self.date = date
        self.cost = cost
        self.detail = detail
        self.category = category
        self.is_in = is_in

    def __str__(self):
        return self.detail + ' ￥' + str(self.cost)
