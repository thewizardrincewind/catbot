import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler

import json

from telegram import ReplyKeyboardMarkup
import random as r

from facts import catfacts

BOT_TOKEN = '5760398094:AAGPczeyvlIUOmfbc2uBNGzL6LPGVC2rbDI'

f = True
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    reply_keyboard = [['/help', '/cat_img'],
                      ['/cat_fact', '/cat_quote']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я кошачий инфобот. Нажми команду" +
        " /help , чтобы узнать обо мне", reply_markup=markup
    )


async def help(update, context):
    reply_keyboard = [['/help', '/cat_img'],
                      ['/cat_fact', '/cat_quote']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Привет! Я - бот, "
                                    "который может кинуть вам фото "
                                    "смешного кота(команда /cat_img),"
                                    "цитату о котах(/cat_quote)"
                                    " или интересный факт о них(/cat_fact).",
                                    reply_markup=markup)


async def cat_img(update, context):
    reply_keyboard = [['/help', '/cat_img'],
                      ['/cat_fact', '/cat_quote']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    """Отправляет сообщение когда получена команда /cat_img"""
    await context.bot.sendPhoto(update.message.chat.id,
                                open(f'data/{r.randint(1, 24)}.jpg', 'rb'),
                                caption='Держи!')


async def stop(update, context):
    reply_keyboard = [['/help', '/cat_img'],
                      ['/cat_fact', '/cat_quote']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text('Команда отменена!',  reply_markup=markup)
    return ConversationHandler.END


async def cat_fact(update, context):
    reply_keyboard = [['/help', '/cat_img'],
                      ['/cat_fact', '/cat_quote']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    reply_keyboard = [['/help', '/cat_img'],
                      ['/cat_fact', '/cat_quote']]

    """Отправляет сообщение когда получена команда /cat_fact"""
    await update.message.reply_text(r.choice(catfacts),  reply_markup=markup)


async def cat_quote(update, context):
    reply_keyboard = [['/add_quote'], ['/help', '/cat_img'],
                      ['/cat_fact', '/cat_quote']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    """Отправляет сообщение когда получена команда /cat_quote"""

    with open('quotes.json') as file:
        f = json.load(file)
        k = list(f.keys())
        one = r.choice(k)
        await update.message.reply_text(str(f[one]) + f' - {one}.' + '\n ________'
                                                              '_____\n Хотите добавить свою '
                                                              'цитату? Используйте команду '
                                                              '/add_quote',  reply_markup=markup)


async def add_quote(update, context):
    reply_keyboard = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text('Введите цитату! (Нажмите /stop, '
                                    'чтобы отменить действие)', reply_markup=markup)

    return 2


async def second_response(update, context):
    user = update.message.from_user
    res = update.message.text
    with open('quotes.json') as file:
        f = json.load(file)
        if user.mention_html() in f.keys():
            await update.message.reply_text(
                f"Извините, но можно загрузить только одну цитату!")
        else:
            f[user['username']] = res
            with open('quotes.json', 'w') as wf:
                json.dump(f, wf, ensure_ascii=False)
    reply_keyboard = [['/help', '/cat_img'],
                      ['/cat_fact', '/cat_quote']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        f"Принято!",  reply_markup=markup)
    return ConversationHandler.END


conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('add_quote', add_quote)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )


def main():
    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    reply_markup = markup
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()
    # Регистрируем обработчик в приложении.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("cat_img", cat_img))
    application.add_handler(CommandHandler("cat_quote", cat_quote))
    application.add_handler(CommandHandler("cat_fact", cat_fact))
    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()