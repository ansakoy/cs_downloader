from telegram.ext import Updater, MessageHandler, Filters
from csdbot_token import TOKEN


def doc_handler(bot, update):
    print('worked')
    received_file = bot.getFile(update.message.document.file_id)
    print("file_id: " + str(update.message.document.file_id))
    received_file.download('params_csv')






if __name__ == '__main__':
    # Регистрация команд и запуск бота
    # updater = Updater(token=TOKEN)
    # dispatcher = updater.dispatcher
    # fromfile_handler = CommandHandler('fromf', fromfile)
    # dispatcher.add_handler(fromfile_handler)
    # updater.start_polling()
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.document, doc_handler))
    updater.start_polling()