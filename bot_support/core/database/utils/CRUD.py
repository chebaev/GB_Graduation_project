import logging

from typing import Dict, List, TypeVar, Any

from loguru import logger
from sqlalchemy import insert, select
from sqlalchemy.exc import ProgrammingError

from core.database.utils.database import engine, session_factory
from core.database.common.models import Base, Support
from core.settings.settings import settings


T = TypeVar('T')

@logger.catch
def _all_create_tables():
    """
    Проверка БД на сервере
    :return:
    """
    try:
        Base.metadata.create_all(engine)
        logging.info(f'Database created "{settings.db_name}"')
    except ProgrammingError:
        logging.error(f'Database with name "{settings.db_name}" does not exist')

@logger.catch
def _store_date(model: T, *data: List[Dict]):
    """
        Запись в базу данных
        :param db:
        :param model:
        :param data:
        :return:
        """
    with session_factory() as conn:
        conn.execute(insert(model).values(*data))
        conn.commit()

@logger.catch
def _get_all_data(model: T) -> Any:
    """
    Чтение из базы данных получение всех данных
    :param model:
    :return:
    """
    with session_factory() as conn:
        result = conn.execute(select(model)).all()
    return result

@logger.catch
def _get_answer_id(_id: int) -> Any:
    """
    Получить данные по id
    :param id:
    :return:
    """
    with session_factory() as conn:
        query = conn.execute(select(Support.answer).where(Support.id == _id)).scalar()
        return query

@logger.catch
def _get_id_questions():

    """
       Функция нужна для обработки ответа
       :return:
       """
    data = {}
    with session_factory() as conn:
        support = conn.execute(select(Support.id, Support.questions, Support.answer))
        result = support.all()
        for value in result:
            elem = tuple(value[1].split(": "))
            data[value[0]] = elem
        return data



class CRUDInterface():
    @staticmethod
    def create_tables():
        return _all_create_tables

    @staticmethod
    def add_data():
        return _store_date

    @staticmethod
    def get_all_data():
        return _get_all_data

    @staticmethod
    def get_answer_id():
        return _get_answer_id

    @staticmethod
    def get_id_questions():
        return _get_id_questions

if __name__ == '__main__':
    _all_create_tables()
    _store_date()
    _get_all_data()
    _get_answer_id()
    _get_id_questions