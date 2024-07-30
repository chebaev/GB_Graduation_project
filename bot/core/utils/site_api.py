import json
import requests

from core.settings.settings import settings
from loguru import logger



def _cookies() -> str:
    """
    Получить cookies с сесии
    """
    params = {
        'username': settings.api_username,
        'password': settings.api_password.get_secret_value()
    }
    url = f'{settings.api_url}/shakalaka/login'
    response = requests.post(url=url, params=params)
    return response.cookies

def _make_response(method: str, url: str, params: dict, func = _cookies, success=200):
    """
    Общая функция для API запросов
    :param method:
    :param url:
    :param params:
    :param func:
    :param success:
    :return:
    """
    resource = requests.request(
        method,
        url,
        params=params,
        cookies=func()
    )
    status_code = resource.status_code
    if status_code == success:
        return resource

    return status_code


def get_user(user: str, func=_make_response) -> dict:
    """Получение данных о пользователе"""
    url = f'{settings.api_url}/shakalaka/panel/api/inbounds/getClientTraffics/{user}'
    response = func("GET", url=url, params={})
    return response.json()
    # response = requests.get(url + "/shakalaka/panel/api/inbounds/getClientTraffics/"+user, cookies=cookies)
    # return response.json()

def get_list(func=_make_response) -> dict:
    """Получение полного списка клиентов и настроек
       url (str): _description_
       cookies (str): _description_
   Returns:
        dict: _description_
    """
    try:
        url = f'{settings.api_url}/shakalaka/panel/api/inbounds/list'
        response = func("GET", url=url, params={})
        return response.json()
    except requests.exceptions.JSONDecodeError:
        logger.error('Не удалось получить список клиентов с сервиса XRAY')

def _add_user_site(telegram_id: str, uuid: str, expiryTime:  int, func=_make_response):
    """Добавление нового пользователя на сервер"""

    try:
        data = {
            "clients": [
                {
                    "email": telegram_id,
                    "enable": True,
                    "flow": "xtls-rprx-vision",
                    "id": uuid,
                    "limitIp": "3",
                    "expiryTime": expiryTime

                }
            ]
        }


        params = {"id": 1, "settings": json.dumps(data)}
        url = f'{settings.api_url}/shakalaka/panel/api/inbounds/addClient'
        return func("POST", url=url, params=params)
    except:
        logger.error(f'Запись нового пользователя {telegram_id} Невозможно.\n '
                     f'Причина нет доступа к сервису XRAY')

def _update_user(telegram_id: str, uuid: str, enable: bool, expiryTime:int = 0, func=_make_response):
    """
    Доработать

    :param url:
    :param data:
    :param uuid:
    :param cookies:
    :return:
    """
    data = {
        "clients": [
            {
                'email': telegram_id,
                "enable": enable,
                "flow": "xtls-rprx-vision",
                "id": uuid,
                "limitIp": "3",
                "expiryTime": expiryTime

            }
        ]
    }
    # session = requests.session()
    url = f'{settings.api_url}/shakalaka/panel/api/inbounds/updateClient/{uuid}'
    params = {"id":1, "settings": json.dumps(data)}
    return func("POST", url=url, params=params)

def _connection_string(id_telegram:str, uuid: str ) -> str:
    """
    Функция отвечает за получение данных с сервиса
    :param id_telegram:
    :param uuid:
    :return:
    """
    try:
        list = json.loads((get_list()['obj'][0]['streamSettings']))
        network = list["network"]
        serverNames = list['realitySettings']['serverNames'][0]
        shortIds = list['realitySettings']['shortIds'][0]
        fingerprint = list['realitySettings']['settings']['fingerprint']
        publicKey = list['realitySettings']['settings']['publicKey']
        security = list['security']
        spiderX = list['realitySettings']['settings']['spiderX']
        if spiderX == '/':
            spiderX = '%2F'
        flow = settings.api_flow
        uuid = uuid
        id_telegram = id_telegram
        link = (
            f'vless://{uuid}@{settings.api_link}?type={network}&security={security}&pbk={publicKey}'
            f'&fp={fingerprint}&sni={serverNames}'
            f'&sid={shortIds}&spx={spiderX}&flow={flow}#{id_telegram}')
        return link
    except TypeError:
        logger.error(f'Нет подключения к сервису XRAY')
def _user_attribute(telegram_id: str, element: str) -> bool:
    """

    :param telegram_id:
    :param element: 'email', 'enable',
    :return:
    """
    try:
        return get_user(telegram_id)['obj'][element]

    except TypeError:
        return None


class SiteApiInterface():

    @staticmethod
    def add_user():
        return _add_user_site

    @staticmethod
    def connection_link():
        return _connection_string

    @staticmethod
    def set_user():
        return _update_user
    @staticmethod
    def get_user_attribute():
        return _user_attribute

site_api = SiteApiInterface()


if __name__ == '__main__':
    # print(get_user(895894170))
    print(_add_user_site('895894170', 'e95ea0de-2688-45a5-bedc-4490e302600f', 1731239081), )
