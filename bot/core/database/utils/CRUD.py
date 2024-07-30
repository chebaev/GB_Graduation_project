from loguru import logger
from typing import Dict, List, TypeVar, Any

from sqlalchemy import insert, select, update, func, text
from sqlalchemy.exc import ProgrammingError, IntegrityError

from core.database.utils.database import engine, session_factory
from core.database.common.models import Base, AdminPanelTab
from core.settings.settings import settings
from core.database.common.models import User, Order
from core.state.state_date import AdminPanel

T = TypeVar('T')
def _store_date(model: T, *data: List[Dict]):
    """
        Запись в базу данных
        :param db:
        :param model:
        :param data:
        :return:
        """
    try:
        with session_factory() as conn:
            conn.execute(insert(model).values(*data))
            conn.commit()
    except:
        logger.error(f'Запись в базу данных не произошла.')
def _get_all_data(model: T )->Any:
    """
    Чтение из базы данных получение всех данных
    :param model:
    :return:
    """
    with session_factory() as conn:
        result = conn.execute(select(model)).scalars().all()
    return result
def _insert_admin_panel(*data: List[Dict]):

    try:

        with session_factory() as conn:

            conn.execute(insert(AdminPanelTab).values(*data))
            conn.commit()
            # stmt = """INSERT INTO adminpanels_tab VALUES (1, 7, 2, ' ', 0, 10, 20, 30)"""
            # conn.execute(text(stmt))
    except IntegrityError:
            logger.info(f"Дублирующая запись '1' для ключа adminpanels_tab.PRIMARY. \n"
                         f"Запись уже существует. Это не ошибка просто бота перезагрузили.")


def _all_create_tables():
    try:
        Base.metadata.create_all(engine)
        logger.info(f'Database created "{settings.db_name}"')

    except ProgrammingError:
        logger.error(f'Database with name "{settings.db_name}" does not exist')






def _user_verification(model: T, telegram_id: str) -> bool:
    """
    Проверка пользователя в базе данных
    :param model:
    :param telegram_id:
    :return:
    """
    with session_factory() as conn:
        result = conn.execute(select(model.telegram_id).where(model.telegram_id == telegram_id)).scalar()
    if result:
        res = True
    else:
        res = False
    return res

def _user_time_check(model: T, telegram_id: str) -> bool:
    """
    Проверка stop_days_left в базе данных вернет bool
    :param model:
    :param telegram_id:
    :return:
    """
    with session_factory() as conn:
        result = conn.execute(select(model.stop_days_left).where(model.telegram_id == telegram_id)).scalar()
    if result > 0:
        res = True
    else:
        res = False
    return res
def _update_data(model: T, telegram_id: str,  *data: List[Dict]):
    """
    Обновление записей в таблице
    :param model:
    :param telegram_id:
    :param data:
    :return:
    """
    with session_factory() as conn:
        conn.execute(update(model)
                     .values(*data)
                     .where(model.telegram_id == telegram_id))
        conn.commit()

def _update_adminpanel(*data: List[Dict]):
    """
    Обновление записей в таблице AdminPanelTab
    :param data:
    :return:
    """
    with session_factory() as conn:
        conn.execute(update(AdminPanelTab)
                     .values(*data)
                     .where(AdminPanelTab.id == 1))
        conn.commit()

def _how_many_users(model: T):
    """
    Количество пользователей
    :param model:
    :return:
    """
    with session_factory() as conn:
        result = conn.query(func.count(model.telegram_id)).scalar()
    return result

def _get_columns_data(model: T, telegram_id: str, column: Any) -> Any:
    """
    Получение значения по колонке
    :param model:
    :param telegram_id:
    :param column:
    :return:
    """

    with session_factory() as conn:
        result = conn.execute(select(column).where(model.telegram_id == telegram_id)).scalar()

    return result

# def _demo_recording_check(model: T)

def _get_orders(telegram_id:str) -> Any:

    with session_factory() as conn:
        query = select(Order.created_date, Order.telegram_id, Order.money).where(Order.telegram_id == telegram_id)
        result = conn.execute(query).all()
        return result

def _get_user_check_shutdown():
    with session_factory() as conn:
        query = select(User.telegram_id, User.status, User.seconds_left)
        return conn.execute(query).all()

def _before_shutdown():
    with session_factory() as conn:
        query = select(User.telegram_id, User.status, User.access_levels, User.seconds_left, User.before_shutdown)
        return conn.execute(query).all()

def _user_check(telegram_id: str):
    with session_factory() as conn:
        query = select(User.status, User.access_levels, User.seconds_left).where(User.telegram_id == telegram_id)
        return conn.execute(query).all()

def _get_monthly_report():
    with session_factory() as conn:
        query = (f"SELECT sum(money) FROM orders WHERE created_date >= DATE_FORMAT(NOW(), '%Y-%m-01')"
                 f" AND created_date < DATE_FORMAT(NOW(), '%Y-%m-01') + INTERVAL 1 MONTH;")

        return conn.execute(text(query)).scalar()

def _report_for_period(start_date:str, end_date:str):
    with session_factory() as conn:
        query = (f"SELECT sum(money) FROM orders WHERE created_date BETWEEN '{start_date}' "
                 f"AND ('{end_date}' + INTERVAL 1 day);")
        return conn.execute(text(query)).scalar()


class CRUDInterface():
    @staticmethod
    def adding_data():
        return _store_date
    @staticmethod
    def set_admin_panel():
        return _insert_admin_panel

    @staticmethod
    def create_tables():
        return _all_create_tables

    @staticmethod
    def get_all_data():
        return _get_all_data

    @staticmethod
    def get_filter_users():
        return _user_verification

    @staticmethod
    def get_time_check():
        return _user_time_check

    @staticmethod
    def update():
        return _update_data

    @staticmethod
    def get_how_many_users():
        return _how_many_users

    @staticmethod
    def get_data():
        return _get_columns_data
    @staticmethod
    def get_order():
        return _get_orders

    @staticmethod
    def get_user_shutdown():
        return _get_user_check_shutdown

    @staticmethod
    def get_monthly_report():
        return _get_monthly_report

    @staticmethod
    def get_report_for_period():
        return _report_for_period
    @staticmethod
    def get_before_shutdown():
        return _before_shutdown

    @staticmethod
    def get_user_check():
        return _user_check
    @staticmethod
    def update_adminpanel():
        return _update_adminpanel

if __name__ == '__main__':
   _store_date()
   _all_create_tables()
   _get_all_data()
   _user_verification()
   _user_time_check()
   _update_data()
   _how_many_users()
   _get_columns_data()
   _get_user_check_shutdown()
   _get_monthly_report()
   _report_for_period()
   _before_shutdown()
   _user_check()
   _insert_admin_panel()
   _update_adminpanel()


