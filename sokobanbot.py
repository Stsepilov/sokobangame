import telebot
from telebot import types
from random import randint

bot = telebot.TeleBot('1703375312:AAGllsrXniJtGZLZb7aXJPOI1vv1ZuX9YEw')


def show_map(gmap):
    gmap_width = str(gmap.find(u'█\n') + 1)
    btn = types.InlineKeyboardButton
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        btn('', callback_data='0'),
        btn(u'⬆', callback_data='-' + gmap_width),
        btn(u'⬅', callback_data='-1'),
        btn(u'➡', callback_data='1'),
        btn('', callback_data='0'),
        btn(u'⬇', callback_data=gmap_width),
    )
    return {
        'text': '<code>' + gmap + '</code>',
        'reply_markup': markup,
        'parse_mode': 'html',
    }


@bot.message_handler(content_types=['text'])
def any_msg(message):
    d = randint(1, 2)
    if d == 1:
        gmap = u"""
            ██████████
            ██████ . █
            █  ◯ᾃ◯ ◯ █
            █     ..██
            ██████████
        """.replace('\n        ', '\n')
    elif d == 2:
        gmap = u"""
            ██████████
            █████.    █
            █ᾃ◯    ◯ █
            █.  ◯   .██
            ██████████
                """.replace('\n        ', '\n')
    bot.send_message(message.chat.id, **show_map(gmap))


def replace_on_map(game_map, pos, char):
    return game_map[:pos] + char + game_map[pos + 1:]


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        gmap = call.message.text
        movement = int(call.data)

        pos = gmap.find(u'ᾃ')
        if pos < 0:
            pos = gmap.find(u'ᾇ')

        new_pos = pos + movement
        new_place = gmap[new_pos]
        next_place = gmap[new_pos + movement]

        if new_place in (' ', '.') or (new_place in (u'◯', u'◉') and next_place in (' ', '.')):
            if new_place in (u'◯', u'◉'):
                gmap = replace_on_map(gmap, new_pos + movement, u'◉' if next_place == '.' else u'◯')
            gmap = replace_on_map(gmap, pos, ' ' if gmap[pos] == u'ᾃ' else '.')
            gmap = replace_on_map(gmap, new_pos, u'ᾃ' if new_place in (' ', u'◯') else u'ᾇ')

        if gmap != call.message.text:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                **show_map(gmap)
            )


bot.polling(none_stop=True)
