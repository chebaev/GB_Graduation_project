import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import SecretStr, StrictStr

load_dotenv()
class Settings(BaseSettings):
    db_name: StrictStr = os.getenv('DATABASE_NAME', None) # Название базы данных
    db_host: StrictStr = os.getenv('DB_HOST', None) # URL-адрес базы данных
    db_user: SecretStr = os.getenv("DB_USER", None)
    db_password: SecretStr = os.getenv("DB_PASSWORD", None)
    db_port: int = int(os.getenv('DB_PORT', None))

    polling_time: int = int(os.getenv('POLLING_TIME', None))

    url_news: StrictStr = os.getenv('URL_NEWS', None)
    url_support: StrictStr = os.getenv('URL_SUPPORT', None)
    offer_url: StrictStr = os.getenv('OFFER_URL', None)
    hellp_url: StrictStr = os.getenv('HELP_URL', None)

    # demo_days: int = int(os.getenv('DEMO_ACCESS_DAYS', None))

    api_url: StrictStr = os.getenv('API_URL', None)
    api_link: StrictStr = os.getenv('API_LINK', None)
    api_flow: StrictStr = os.getenv('API_FLOW', None)
    api_username: StrictStr = os.getenv('API_USERNAME', None)
    api_password: SecretStr = os.getenv('API_PASSWORD', None)

    token: SecretStr = os.getenv("TOKEN", None)
    admin_id: SecretStr = os.getenv("ADMIN_ID", None)
    admins_id_group: StrictStr = os.getenv("ADMINS_ID_GROUP", None)


    bot_nickname: StrictStr = os.getenv("BOT_NICKNAME", None)
    bot_name: StrictStr = os.getenv("BOT_NAME", None)

    yootoken: SecretStr = os.getenv("YOOTOKEN", None)



    days_month: int = int(os.getenv('DAYS_MONTH', None))
    # money_a_day: float = float(os.getenv('MONEY_A_DAY', None))

    referrer_money: float = float(os.getenv('REFERRER_MONEY', None))
    referrer_day: int = int(os.getenv('REFERRER_DAY', None))

    @property
    def DATABASE_URL_MYSQL_asyncmy(self):
        return (f"mysql+mysqlconnector://{self.db_user.get_secret_value()}:{self.db_password.get_secret_value()}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}")

settings = Settings()
