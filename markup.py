from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
import db

def markup_admin():
        markup_admin = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
                KeyboardButton(text="Рассылка"),
                KeyboardButton(text="Изменить приветствие"),
                KeyboardButton(text="Изменить каналы"),
                KeyboardButton(text="Изменить курс"),
                KeyboardButton(text="Заявки"),
                KeyboardButton(text="Статистика"),
                KeyboardButton(text="Откл/вкл реф ссылку"),
                KeyboardButton(text="Изменить 2 приветствие"),
                ]
        markup_admin.add(*buttons)
        return markup_admin
def markup(user_id,money):
        markup = InlineKeyboardMarkup()
        buttons = [
                KeyboardButton(text="Принять",callback_data=f'yes_{user_id}_{money}'),
                KeyboardButton(text="Отклонить",callback_data=f'no_{user_id}_{money}'),
        ]
        markup.add(*buttons)
        return markup

def markup_user():
        markup_admin = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
                KeyboardButton(text="Заработать"),
                KeyboardButton(text="Личный кабинет"),
                KeyboardButton(text="Вывести"),
        ]
        markup_admin.add(*buttons)
        return markup_admin

def markup1():
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        KeyboardButton(text="STANDOFF 2",callback_data='next1'),
        KeyboardButton(text="Private V2", callback_data='next1'),
        KeyboardButton(text="Project Evolution", callback_data='next1'),
        KeyboardButton(text="Stand Knife", callback_data='next1'),
        KeyboardButton(text="Private Snak", callback_data='next1'),
        KeyboardButton(text="Stand Leo", callback_data='next1'),
        KeyboardButton(text="Stand Chillow", callback_data='next1'),
        KeyboardButton(text="Stand Rise", callback_data='next1'),
    ]
    markup.add(*buttons)
    return markup
def markup2():
    sub = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for channel in db.channels():
        buttons.append(KeyboardButton(text="ПОДПИСАТЬСЯ",url = channel[0]))
    buttons.append(KeyboardButton(text="☑️ Проверить подписку", callback_data='next2'))
    sub.add(*buttons)
    return sub,db.channels()




