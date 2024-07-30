from core.database.common.models import User
from core.database.core import crud

db_user_data = crud.get_data()
def get_status(telegram_id: str) -> str:
    if db_user_data(User, telegram_id, User.status):
        result = 'активный'
    else:
        result = 'не активный'
    return result