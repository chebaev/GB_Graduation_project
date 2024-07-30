import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import SecretStr, StrictStr, StrictFloat, StrictInt
load_dotenv()

class Settings(BaseSettings):
    token: SecretStr = os.getenv("TOKEN", None)
    admin_id: SecretStr = os.getenv("ADMIN_IDS", None)
    group_id: int = int(os.getenv("GROUP_ID", None))
    bot_name: StrictStr = os.getenv("BOT_NAME", None)

    db_name: StrictStr = os.getenv('DATABASE_NAME', None) # Название базы данных
    db_host: StrictStr = os.getenv('DB_HOST', None) # URL-адрес базы данных
    db_port: int = int(os.getenv('DB_PORT', None))
    db_user: SecretStr = os.getenv("DB_USER", None)
    db_password: SecretStr = os.getenv("DB_PASSWORD", None)

    @property
    def DATABASE_URL_MYSQL_asyncmy(self):
        return (f"mysql+mysqlconnector://{self.db_user.get_secret_value()}:{self.db_password.get_secret_value()}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}")






settings = Settings()

