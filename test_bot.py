import time


def test_bot(bot, sleep, chat_id):
    time.sleep(int(sleep))
    message = 'slept for %s seconds' % sleep
    bot.send_message(chat_id=chat_id, text=message)
