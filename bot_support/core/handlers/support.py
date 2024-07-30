import re
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from loguru import logger

from core.keyboards.inline.support_inline import keyboard_support, keyboard_support_not_save
from core.settings.settings import settings
from core.state.register import RegAnswer
import core.utils.functions as fc

from core.database.core import crud
from core.database.common.models import Support

db_get_id_questions = crud.get_id_questions()
db_get_answer = crud.get_answer_id()
db_write_data = crud.add_data()



@logger.catch
async def get_wait_message(message: Message, bot: Bot, state: FSMContext):
    """
    Отправка сообщения администратору
    :param message:
    :param bot:
    :return:
    """
    question = " "
    if message.chat.id != settings.group_id:
        if message.text:
            question = message.text
            answer_id = fc.recognize_questio(message.text, db_get_id_questions())

            if answer_id > 0:
                await bot.send_message(message.from_user.id, db_get_answer(answer_id))
            else:
                await state.update_data(question=question)

                await bot.send_message(chat_id=settings.group_id, text=f"Telegram_id: {message.from_user.id}\n"
                                                                       f"<b>От:</b> {message.from_user.first_name}\n"
                                                                       f"<b>Вопрос:</b> {question}"
                                       , reply_markup=keyboard_support)
                await bot.send_message(message.from_user.id, "Ваше сообщение было отправлено в службу тех. поддержки.")

        elif not message.text:
            if message.photo:
                question = "Фото"
            elif message.document:
                question = "Документ"
            elif message.animation:
                question = "Анимация"
            elif message.voice:
                question = "Голосовое сообщение"
            elif message.video:
                question = "Видео"
            await bot.forward_message(settings.group_id, message.from_user.id, message.message_id)
            await bot.send_message(chat_id=settings.group_id, text=f"Telegram_id: {message.from_user.id}\n"
                                                                   f"От: {message.from_user.first_name}\nВопрос: {question}",
                                   reply_markup=keyboard_support_not_save)
            await bot.send_message(message.from_user.id, "Ваше файл был отправлен в службу тех. поддержки.")
@logger.catch
async def reply_to_user_save(callback: CallbackQuery, state: FSMContext):
    """
    Срабатывает когда админ нажимает на кнопку 'Ответить с сохранением в БД'
    :param callback:
    :param state:
    :return:
    """

    await state.update_data(question=callback.message.text)

    user_data = await state.get_data()
    question = user_data.get('question')
    await state.update_data(activity=True)
    await callback.message.delete()
    await callback.message.answer(f'{question}\n<b>Введите ответ (он сохранится в БД):</b>')
    await state.set_state(RegAnswer.answer)

@logger.catch
async def reply_to_user(callback: CallbackQuery, state: FSMContext):
    """
    Срабатывает когда админ нажимает на кнопку 'Ответить пользователю'
    :param callback:
    :param state:
    :return:
    """
    await state.update_data(question=callback.message.text)
    await state.update_data(activity=False)
    user_data = await state.get_data()
    question = user_data.get('question')
    await callback.message.delete()
    await callback.message.answer(f'{question}\n<b>Введите ответ :</b>')
    await state.set_state(RegAnswer.answer)

@logger.catch
def get_question(text: str) -> str:
    """
    Функция: выбирает из строки только вопрос от пользователя
    :param text:
    :return:
    """
    pattern = 'Вопрос: '
    result = re.split(pattern, text)[1]
    return result
@logger.catch
def get_telegram_id(text:str) -> int:
    """
    Функция: Из строки взять только цифры telegram ID
    :param text:
    :return:
    """
    result = re.findall(r'\b\d+\b', text)
    number = list(map(int, result))[0]
    return number
@logger.catch
async def state_admin(message: Message, bot: Bot, state: FSMContext):
    """
    Срабатывает когда администратор отправляет сообщение
    :param message:
    :param state:
    :param bot:
    :return:
    """
    user_data = await state.get_data()
    result = user_data.get('question')
    question = get_question(result)
    activity = user_data.get('activity')
    if activity:
        data = {
            'questions': question,
            'answer': message.text
        }
        db_write_data(Support, data)
    await bot.send_message(chat_id=get_telegram_id(result), text=f'<b>На вопрос:</b> {question}\n'
                                                                   f'<b>Ответ от тех.поддержки:</b>\n{message.text}')
    await state.clear()

