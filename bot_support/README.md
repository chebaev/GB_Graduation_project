# Бот для технической поддержки пользователей.

Представлен бот тех поддержки. Устанавливается бот, создаётся группа в Telegram.
И в этой группе добавляем в администраторы имя бота. Узнаём id Telegram группы и
прописываем в файл .env добавляя спереди -100 

Установить зависимости
> pip install -r requirements.txt

Создать файл .core/settings/.env все настойки взять в файле .core/settings/.env.example 

Основные команды 
- /start

## Принцип работы
При отправке сообщения от пользователя проверяется в базе данных такие же 
вопросы и, если есть варианты совпадения более 70 % отсылает ответ 
(за это отвечает библиотека "fuzzywuzzy").
Ели нет подходящих вопросов, то автоматически пересылается в группу.
