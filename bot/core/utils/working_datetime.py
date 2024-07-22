import time
import datetime
import re

def days_to_seconds(days: int) -> int:
    """
    Функция преобразует дни в секунды
    days: дни
    """
    return days * 24 * 60 * 60

def set_left_days_in_seconds():
    pass
def number_of_digits(seconds:int) -> int:
    """
    Проверка сколько цифр
    """
    time_now = int(time.time())
    if len(str(seconds)) > 10:
        seconds = seconds // 1000
        result = int(seconds) - time_now
    elif len(str(seconds)) == 10:
        result = int(seconds) - time_now
    else:
        result = seconds
    return result

def get_left_days_in_seconds(get_time):
    """
    Получение сколько дней и часов осталось
    """
    pattern_1 = r'(^[0-9]{2}\:[0-9]{2}\:[0-9]{2})'
    pattern_2 = r'(^[0-9]\:[0-9]{2}\:[0-9]{2})'
    middle_time = number_of_digits(get_time)


    if middle_time <= 0:
        result = f'0 дней'
    else:
        result = str(datetime.timedelta(seconds=middle_time))
        if (re.findall(pattern_1, result)) or (re.findall(pattern_2, result)):
            result = result

        else:
            summ = (int(result.split()[0]))
            if summ == 1:
                if result.split()[1] == "day,":
                    result = result.replace("day", "день")
                else:
                    result = result.replace("days", "день")
            elif 1 < summ < 5:
                result = result.replace("days", "дня")
            else:
                result = result.replace("days", "дней")
    return result





