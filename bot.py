import time

from aiogram import types, Bot, executor
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import asyncio

import datetime

import os

import db

import classes
import markup

admin = #user id админа

name_bot = ''#Название бота

bot = Bot(token="")#Токен бота
# Диспетчер
dp = Dispatcher(bot,storage=MemoryStorage())

def check_sub_channel(chat_member):
    if chat_member.status != 'left':
        return True
    else:
        return False

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.id == admin:
        await message.answer('Добро пожаловать в админ панель',reply_markup=markup.markup_admin())
    else:
        text = db.text()
        await message.answer(text, reply_markup=markup.markup1())
        try:
            ref = message.text.split(' ')[1]
            if str(ref) == str(message.chat.id):
                ref = None
        except:
            ref = None
        db.add_beta(message.chat.id,ref)


@dp.message_handler()
async def number(message: types.Message):
    if message.chat.id == admin:
        if message.text == 'Рассылка':
            await message.answer('Напишите текст')
            await classes.Mailing.message.set()
        elif message.text == 'Откл/вкл реф ссылку':
            ref = db.change_ref()

            if ref:
                await message.answer('Реф. ссылка включена')
            elif not ref:
                await message.answer('Реф. ссылка выключена')
        elif message.text == 'Изменить приветствие':
            await message.answer('Напишите текст')
            await classes.change.message.set()
        elif message.text == 'Изменить 2 приветствие':
            await message.answer('Напишите текст')
            await classes.change2.message.set()
        elif message.text == 'Изменить курс':
            await message.answer('Напишите курс')
            await classes.well.message.set()
        elif message.text == 'Заявки':
            if len(db.application()) == 0:
                await message.answer('Заявок нет')
                return
            for application in db.application():
               id = application[0]
               wallet = application[1]
               money = application[2]
               await message.answer(f'Заявка от пользователя {id}\n\nКоличество: {money}\n\nКошелек: {wallet}',reply_markup=markup.markup(id,money))
        elif message.text == 'Изменить каналы':
            await message.answer('Напишите каналы через проблем \n\nПример:https://t.me/...')
            await classes.Channels.channel.set()
        elif message.text == 'Статистика':
            now = datetime.datetime.now()
            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")
            day,month,year = db.statistics(day,month,year)
            await message.answer(f'Рефералов за день: {day} чел \n\nРефералов за месяц: {month} чел \n\nРефералов за год: {year} чел')
        else:
            await message.answer('Я не понял Вас!')
    else:
        try:
            id_user, id_ref = db.beta(message.chat.id)
        except:
            pass
        if message.text == 'Заработать':
            ref = db.ref()
            if ref:
                url = f'http://t.me/{name_bot}?start='
                await message.answer(f'Чтобы заработать, пригласите друзей\n\nВаша ссылка:{url+str(message.chat.id)}')
            elif not ref:
                await message.answer(f'Пока что рефералы не требуются. Мы вернём реф ссылку и оповестим вас когда будут нужны рефералы')
        elif message.text == 'Личный кабинет':
            exchange = db.exchange()
            quant, earned, salary = db.personal_account(message.chat.id)
            earned = "%.4f" % float(earned)
            text = f'Курс за реферала: {exchange}$\nВаш баланс: {earned}$\nВсего приглашено: {quant}\nВсего выплачено: {salary}$'
            await message.answer(text)
        elif message.text == 'Вывести':
            earned = db.personal_account(message.chat.id)[1]
            if float(earned) >= 1:
                await message.answer(f'У вас на счету: {earned}$\nСколько вы хотите вывести?')
                await classes.wallet.message.set()
            else:
                await message.answer('Минимальный вывод 1$')

@dp.message_handler(state=classes.Channels.channel)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(channel=message.text)
    text = await state.get_data()
    db.add_channel(text['channel'])
    await message.answer('Каналы изменены')
    await state.finish()

@dp.message_handler(state=classes.well.message)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    text = await state.get_data()
    db.exchange_uppdate(text['message'])
    await message.answer('Курс изменен')
    await state.finish()

#вывод
@dp.message_handler(state=classes.wallet.message)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await message.answer('Для вывода дайте свой счет в @send или же дайте свою банковскую карту')
    await classes.wallet.wallet_user.set()


#вывод
@dp.message_handler(state=classes.wallet.wallet_user)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(wallet_user=message.text)
    text = await state.get_data()
    try:
        name = '@'+message.from_user.username
    except:
        name = message.from_user.first_name
    text_message = f'Заявка от пользователя {name}\n\nКоличество: {text["message"]}\n\nКошелек: {text["wallet_user"]}'
    await message.answer('🔥Ваша заявка на вывод успешно подана🔥\nВывод воспроизводится в течении 1 дня')
    db.application_add(message.chat.id,text["wallet_user"],text["message"])
    await bot.send_message(admin,text_message,reply_markup=markup.markup(message.chat.id,text["message"]))
    await state.finish()




#рассылка
@dp.message_handler(content_types=types.ContentType.PHOTO,state=classes.Mailing.message)
async def process_name(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    name = 'photo_mailing.jpg'
    await photo.download(destination=name)
    await state.update_data(message=message.caption)
    text = await state.get_data()
    with open(name, 'rb') as phot:
        photo_data = phot.read()
    for user in db.users():
        try:
            await bot.send_photo(user[0],photo=photo_data,caption=text['message'])
        except:
            pass
    os.remove(name)
    await message.answer('Рассылка сделана')
    await state.finish()

#приветсвие
@dp.message_handler(state=classes.change.message)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    text = await state.get_data()
    await message.answer('Приветствие изменено')
    db.change(text['message'])
    await state.finish()

@dp.message_handler(state=classes.change2.message)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    text = await state.get_data()
    await message.answer('2-ое приветствие изменено')
    db.change2(text['message'])
    await state.finish()


@dp.callback_query_handler(text='next1')
async def next_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('➕ Отправьте ID аккаунта на который выводить х5000G:')
    await classes.Trash.message.set()

@dp.message_handler(state=classes.Trash.message)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    text = await state.get_data()
    await state.finish()
    sent_message = await message.answer('⚪️-⚪️-⚪️-⚪️-⚪️-⚪️-⚪️-⚪️-⚪️-⚪️\n└ 0% - собираем данные')
    await asyncio.sleep(1)
    await bot.edit_message_text(
        '🌐-🌐-⚪️-⚪️-⚪️-⚪️-⚪️-⚪️-⚪️-⚪️\n└ 20% - анализируем данные',
        chat_id=message.chat.id,
        message_id=sent_message.message_id
    )
    await asyncio.sleep(1)
    await bot.edit_message_text(
        '🌐-🌐-🌐-🌐-⚪️-⚪️-⚪️-⚪️-⚪️-⚪️\n└ 40% - соединяемся с сервером',
        chat_id=message.chat.id,
        message_id=sent_message.message_id
    )
    await asyncio.sleep(1)
    await bot.edit_message_text(
        '🌐-🌐-🌐-🌐-🌐-🌐-⚪️-⚪️-⚪️-⚪️\n└ 60% - выгружаем данные',
        chat_id=message.chat.id,
        message_id=sent_message.message_id
    )
    await asyncio.sleep(1)
    await bot.edit_message_text(
        '🌐-🌐-🌐-🌐-🌐-🌐-🌐-🌐-⚪️-⚪️\n└ 80% - ищем ваш аккаунт',
        chat_id=message.chat.id,
        message_id=sent_message.message_id
    )
    await asyncio.sleep(1)
    await bot.edit_message_text(
        '🌐-🌐-🌐-🌐-🌐-🌐-🌐-🌐-🌐-🌐\n└ 100% - аккаунт найден!',
        chat_id=message.chat.id,
        message_id=sent_message.message_id
    )
    await asyncio.sleep(1)
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)
    text = db.text2()
    await message.answer(text,reply_markup=markup.markup2()[0])

@dp.callback_query_handler(text='next2')
async def next_menu(callback: types.CallbackQuery):
    for i in markup.markup2()[1]:
        id = i[0]
        if i[1] != None:
            id = i[1]
        else:
            id = id.replace('https://t.me/', '@')
        if not check_sub_channel(await bot.get_chat_member(chat_id=id, user_id=callback.message.chat.id)):
            await callback.message.answer('Пожалуйста, подпишитесь на каналы')
            return

    try:
        now = datetime.datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        id = db.beta(callback.message.chat.id)
        id_user, id_ref = id[0], id[1]
        db.add(id_user, id_ref, year, month, day)
        await callback.message.answer('☑️Мы отправим вам голду всем по очереди ваше место в очереди: 4500', reply_markup=markup.markup_user())
    except:
        await callback.message.answer('Вы уже зарегистрированы', reply_markup=markup.markup_user())
        return
    try:
        await bot.send_message(id_ref, 'Пользователь зарегистрирован по вашей реф. ссылке')
    except:
        pass

@dp.callback_query_handler()
async def next_menu(callback: types.CallbackQuery):
    text = callback.data.split('_')
    first = text[0]
    id = text[1]
    money = text[2]
    if first == 'yes':
        db.withdraw(id,money)
        await callback.message.answer('Вы приняли платеж')
        await callback.message.delete()
        await bot.send_message(id,'Вывод успешно воспроизведен!')
    elif first == 'no':
        await callback.message.answer('Вы отклонили платеж')
        await callback.message.delete()
        await bot.send_message(id, 'Вам отклонен платеж')
    db.application_delete(id)

executor.start_polling(dp,skip_updates=True)
