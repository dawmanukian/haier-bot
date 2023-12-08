import telebot
from telebot import types
import pymysql
from datetime import date

db = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "haier"
}

bot = telebot.TeleBot('6570372334:AAEKyFRDhFIrp9__3VyZvpFmlITdUepZbh0')

@bot.message_handler(commands=['start'])
def start_command(message):
    file = open('photo_2023-11-20_21-58-27.jpg', 'rb')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('💎 промокод 1%', callback_data='promocode_1')
    btn2 = types.InlineKeyboardButton('💎 промокод 5%', callback_data='promocode_5')
    btn3 = types.InlineKeyboardButton('💎 промокод 15%', callback_data='promocode_15')
    btn4 = types.InlineKeyboardButton('⚠️ условия и пользования промокода', callback_data='terms')
    btn5 = types.InlineKeyboardButton('📞 контакты', callback_data='contact')

    markup.row(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    markup.add(btn5)

    bot.send_photo(message.chat.id, file, '''🤖 Бот для получения скидки на технику HAIER 🤖 

❓Вам нужна техника – Haier всегда рядом!
❕ Доставляем по России бесплатно
❕ Даем расширенную гарантию

ВАЖНО ☝ 
Промокод дает дополнительную скидку и НЕ СОВМЕЩАЕТСЯ с поврежденной упаковкой. 

ПРАВИЛА ПОЛУЧЕНИЯ И ИСПОЛЬЗОВАНИЯ ПРОМОКОДА.  

1) Есть 3 разных вида промокода👇🏽

1% - совмещается с клубной скидкой и можно применить ко всем товарам.

5% - не совмещается с клубной скидкой и только на товар с красным ценником( товар со скидкой на сайте ).

15% - не совмещается с клубной скидкой и подойдет только на товар с черным ценником ( товар без скидки на сайте ).

2) Запрещено продавать промокод .

3) Промокод выдается на 24 часа - на следующие сутки при не использовании бот его отдаст другому .

Промокод можно получить в личном обращении в телеграмм оператору @haieroperator .

<a href='https://t.me/Haiersale'>
<b>Подписывайся на канал</b>
</a>
<a href='https://t.me/haiersalehom'>
<b>Вступай в чат где можно получить отзывы от реальных пользователей</b>
</a>

Остались вопросы задавай их администраторам @markusgut, @haierpromo.''',parse_mode='html',reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    connection = pymysql.connect(**db)
    cursor = connection.cursor()
    if callback.data == 'contact':
        bot.send_message(callback.message.chat.id, """📞 Контакты.
        ---------------------
        Telegram: @markusgut
        Канал: https://t.me/Haiersale
        Чат: https://t.me/haiersalehom""", )
    elif callback.data == 'terms':
        file = open('photo_2023-11-20_22-00-21.jpg', 'rb')
        bot.send_photo(callback.message.chat.id, file, """
        
        ВАЖНО ☝️ 
        Промокод дает дополнительную скидку и НЕ СОВМЕЩАЕТСЯ с поврежденной упаковкой. 
        
        ПРАВИЛА ПОЛУЧЕНИЯ И ИСПОЛЬЗОВАНИЯ ПРОМОКОДА.  
        
        1) Есть 3 разных вида промокода👇🏽
        
        1% - совмещается с клубной скидкой и можно применить ко всем товарам.
        
        5% - не совмещается с клубной скидкой и только на товар с красным ценником( товар со скидкой на сайте ).
        
        15% - не совмещается с клубной скидкой и подойдет только на товар с черным ценником ( товар без скидки на сайте ).
        
        2) Запрещено продавать промокод .
        
        3) Промокод выдается на 24 часа - на следующие сутки при не использовании бот его отдаст другому .""")
    elif callback.data == 'promocode_1':
        select1 = "SELECT * FROM given_codes WHERE user_id = %s AND type = %s AND date = %s"
        cursor.execute(select1, (callback.message.chat.id, 1, date.today()))
        connection.commit()
        data = cursor.fetchone()
        if data == None:
            select = "SELECT * FROM promo WHERE type = %s"
            cursor.execute(select, ('1'))
            connection.commit()
            data = cursor.fetchone()
            if data != None:
                insert = "INSERT INTO given_codes (code, type, user_id, date) VALUES (%s,%s,%s, %s)"
                cursor.execute(insert, (data[1],data[2],callback.message.chat.id, date.today()))
                connection.commit()
                delete = "DELETE FROM promo WHERE id = %s"
                cursor.execute(delete, (data[0]))
                connection.commit()
                bot.send_message(callback.message.chat.id, data[1])
            else:
                bot.send_message(callback.message.chat.id, '✅ Промокоды закончились. Жди пополнения!')
        else:
            bot.send_message(callback.message.chat.id, '⚠️ Вы уже взяли промокод попробуйте завтра ')
    elif callback.data == 'promocode_5':
        select1 = "SELECT * FROM given_codes WHERE user_id = %s AND type = %s AND date = %s"
        cursor.execute(select1, (callback.message.chat.id, 5, date.today()))
        connection.commit()
        data = cursor.fetchone()
        if data == None:
            select = "SELECT * FROM promo WHERE type = %s"
            cursor.execute(select, ('5'))
            connection.commit()
            data = cursor.fetchone()
            if data != None:
                insert = "INSERT INTO given_codes (code, type, user_id, date) VALUES (%s,%s,%s, %s)"
                cursor.execute(insert, (data[1],data[2],callback.message.chat.id, date.today()))
                connection.commit()
                delete = "DELETE FROM promo WHERE id = %s"
                cursor.execute(delete, (data[0]))
                connection.commit()
                bot.send_message(callback.message.chat.id, data[1])
            else:
                bot.send_message(callback.message.chat.id, '✅ Промокоды закончились. Жди пополнения!')
        else:
            bot.send_message(callback.message.chat.id, '⚠️ Вы уже взяли промокод попробуйте завтра ')
    elif callback.data == 'promocode_15':
        select1 = "SELECT * FROM given_codes WHERE user_id = %s AND type = %s AND date = %s"
        cursor.execute(select1, (callback.message.chat.id, 15, date.today()))
        connection.commit()
        data = cursor.fetchone()
        if data == None:
            select = "SELECT * FROM promo WHERE type = %s"
            cursor.execute(select, ('15'))
            connection.commit()
            data = cursor.fetchone()
            if data != None:
                insert = "INSERT INTO given_codes (code, type, user_id, date) VALUES (%s,%s,%s, %s)"
                cursor.execute(insert, (data[1],data[2],callback.message.chat.id, date.today()))
                connection.commit()
                delete = "DELETE FROM promo WHERE id = %s"
                cursor.execute(delete, (data[0]))
                connection.commit()
                bot.send_message(callback.message.chat.id, data[1])
            else:
                bot.send_message(callback.message.chat.id, '✅ Промокоды закончились. Жди пополнения!')
        else:
            bot.send_message(callback.message.chat.id, '⚠️ Вы уже взяли промокод попробуйте завтра ')

bot.infinity_polling()