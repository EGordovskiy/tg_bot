import logging
import os
from config import tg_bot_token
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Задайте токен вашего бота, который вы получили от BotFather в Телеграме.
# BOT_TOKEN = "1758573114:AAGQlXER0-9zbhihioKibcI33L1ofSkT38U"
BOT_TOKEN = tg_bot_token

# Настройка логгера
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Определение состояний для разговора с ботом
PHOTO_CHOICE, VOICE_CHOICE = range(2)


# Функции для команды /start
def start(update: Update, _: CallbackContext) -> int:
    user = update.effective_user
    update.message.reply_text(f"Привет, {user.first_name}! Я бот, который поможет тебе со мной познакомиться. "
                              f"Выбирай интересующую тему из кнопок.",
                              reply_markup=ReplyKeyboardMarkup(
                                  [
                                      [KeyboardButton("Посмотреть селфи"),
                                       KeyboardButton("Посмотреть фото из школы")],
                                      [KeyboardButton("Прочитать об увлечении"),
                                       KeyboardButton("Что такое GPT?")],
                                      [KeyboardButton("SQL vs NoSQL"),
                                       KeyboardButton("История первой любви")],
                                      [KeyboardButton("Ссылка на репозиторий")],
                                      [KeyboardButton("Показать список команд")]],
                                  resize_keyboard=True))


def help_command(update: Update, _: CallbackContext) -> None:
    help_text = "Список доступных команд:\n\n" \
                "/start - Начать разговор с ботом\n" \
                "/selfie - Посмотреть селфи\n" \
                "/school_photo - Посмотреть фото из школы\n" \
                "/hobby - Прочитать об увлечении\n" \
                "/gpt - Что такое GPT?\n" \
                "/sql_vs_nosql - SQL vs NoSQL\n" \
                "/first_love - История первой любви\n" \
                "/repo - Ссылка на репозиторий\n" \
                "/help - Показать список команд\n\n" \
                "Выбирайте интересующую тему из кнопок или используйте команды."



# Функция для команды /selfie
def show_selfie(update: Update, _: CallbackContext) -> int:
    update.message.reply_photo(photo=open('media/1.jpg', 'rb'),
                               caption="Моё последнее селфи!")


# Функция для команды /school_photo
def show_school_photo(update: Update, _: CallbackContext) -> int:
    update.message.reply_photo(photo=open('media/2.jpg', 'rb'),
                               caption="Фото из старшей школы вместе с одноклассниками.")


# Функция для команды /hobby
def read_about_hobby(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Моё главное увлечение - это публичные выступления! "
                              "Это позволяет мне взаимодействовать с миром и решать интересные задачи.")


# Функция для команды /gpt
def explain_gpt(update: Update, _: CallbackContext) -> int:
    update.message.reply_voice(voice=open('media/gpt.ogg', 'rb'),
                               caption="Объясняю своей бабушке, что такое GPT")


# Функция для команды /sql_vs_nosql
def explain_sql_vs_nosql(update: Update, _: CallbackContext) -> int:
    update.message.reply_voice(voice=open('media/sql_nosql.ogg', 'rb'),
                               caption="Максимально коротко объясняю разницу между SQL и NoSQL.")


# Функция для команды /first_love
def first_love_story(update: Update, _: CallbackContext) -> int:
    update.message.reply_voice(voice=open('media/first_love.ogg', 'rb'),
                               caption="История моей первой любви.")


# Функция для команды /repo
def repository(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Мои исходники этого бота на GitHub: "
                              "https://github.com/Egordovskiy/123")


# Функция для неизвестных команд
def unknown(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        "Извините, я не понимаю эту команду. Попробуйте выбрать что-то из вариантов, нажав на кнопку "
        "'Показать список команд' или введя команду '/help'.")


def handle_button_press(update: Update, _: CallbackContext) -> int:
    text = update.message.text
    if text == "Посмотреть селфи":
        return show_selfie(update, _)
    elif text == "Посмотреть фото из школы":
        return show_school_photo(update, _)
    elif text == "Прочитать об увлечении":
        return read_about_hobby(update, _)
    elif text == "Что такое GPT?":
        return explain_gpt(update, _)
    elif text == "SQL vs NoSQL":
        return explain_sql_vs_nosql(update, _)
    elif text == "История первой любви":
        return first_love_story(update, _)
    elif text == "Ссылка на репозиторий":
        return repository(update, _)
    elif text == "Показать список команд":
        return help_command(update, _)
    else:
        return unknown(update, _)


# Главная функция для запуска бота
def main() -> None:
    updater = Updater(BOT_TOKEN)

    # Получение диспетчера для регистрации обработчиков команд
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("selfie", show_selfie))
    dispatcher.add_handler(CommandHandler("school_photo", show_school_photo))
    dispatcher.add_handler(CommandHandler("hobby", read_about_hobby))
    dispatcher.add_handler(CommandHandler("gpt", explain_gpt))
    dispatcher.add_handler(CommandHandler("sql_vs_nosql", explain_sql_vs_nosql))
    dispatcher.add_handler(CommandHandler("first_love", first_love_story))
    dispatcher.add_handler(CommandHandler("repo", repository))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Регистрация обработчика неизвестных команд
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Регистрация обработчика на нажатие кнопок
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_button_press))

    # Запуск бота
    updater.start_polling()

    # Остановка бота по нажатию Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
