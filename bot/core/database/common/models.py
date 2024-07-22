import enum
from datetime import datetime
from typing import Annotated
from sqlalchemy import Text, func, Float, String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from core.database.utils.database import Base, session_factory

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_date = Annotated[datetime, mapped_column(default=func.now())]

class Attribute(enum.Enum):
    demo = 'demo'
    private = 'private'
    admin = 'admin'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    telegram_id: Mapped[str] = mapped_column(String(100), nullable=False)
    uuid: Mapped[str] = mapped_column(Text)
    first_name: Mapped[str] = mapped_column(String(150), default='', nullable=True)
    username: Mapped[str] = mapped_column(String(100), default='', nullable=True)
    email: Mapped[str] = mapped_column(String(150), default='', nullable=True)
    access_levels: Mapped[Attribute] = mapped_column(default=Attribute.demo)
    before_shutdown: Mapped[int] = mapped_column(Integer, default=3)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    blocking_user: Mapped[int] = mapped_column(Integer, default=0)
    stop_days_left: Mapped[int] = mapped_column(Integer, default=0)
    seconds_left: Mapped[int] = mapped_column(Integer, default=0)
    balance: Mapped[float] = mapped_column(Float, default=0)
    connect_link: Mapped[str] = mapped_column(Text, default='')
    referral_link: Mapped[str] = mapped_column(Text, default='')

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[intpk]
    created_date: Mapped[created_date]
    telegram_id: Mapped[str] = mapped_column(String(100), nullable=False)
    money: Mapped[float] = mapped_column(Float, default=0)

    def __repr__(self):
        return f"{self.created_date}, {self.telegram_id}, {self.money}"

    @classmethod
    def get_all_order(cls):
        return session_factory.query(Order).all()


class UserReferrer(Base):
    __tablename__ = 'user_referrer'

    id: Mapped[intpk]
    telegram_id: Mapped[str] = mapped_column(String(100), default=0)
    referrer_id: Mapped[str] = mapped_column(String(100), default=0)

    def __repr__(self):
        return f'{self.telegram_id}, {self.referrer_id}'


class AdminPanelTab(Base):
    __tablename__ = "adminpanels_tab"

    id: Mapped[intpk]
    discount_demo_day: Mapped[int] = mapped_column(Integer, default=7)
    discount_price_day: Mapped[float] = mapped_column(Float, default=2)
    discount_message: Mapped[str] = mapped_column(String(250), default='')
    discount_1_months: Mapped[int] = mapped_column(Integer, default=0)
    discount_3_months: Mapped[int] = mapped_column(Integer, default=10)
    discount_6_months: Mapped[int] = mapped_column(Integer, default=20)
    discount_12_months: Mapped[int] = mapped_column(Integer, default=30)

    def __repr__(self):
        return (f'{self.discount_demo_day}, {self.discount_price_day}, {self.discount_message}, {self.discount_1_months},'
                f'{self.discount_3_months}, {self.discount_6_months}, {self.discount_12_months}')
