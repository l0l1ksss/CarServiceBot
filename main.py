import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from pyexpat.errors import messages
import time
import datetime

from db_insert import *
from keyboards import phone
from states.registration import *

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="")
# Диспетчер
dp = Dispatcher()

server={}

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if check_registration(message.chat.id)==0:
        await message.delete()
        await message.answer("Здравствуйте, зарегистрируйтесь с помощью команды /registration, чтобы продолжить!")
    else:
        await message.delete()
        await message.answer("Здравствуйте!")


@dp.callback_query()
async def inline_echo(callback: types.CallbackQuery, state):
    await state.clear()
    if callback.data=="garage":
        await garage(callback.message, state)
    elif callback.data[:10] == "puthistory":
        server[callback.message.chat.id]=callback.data[10:]
        clear_history(server[callback.message.chat.id])
        await callback.message.delete()
        await callback.message.answer("Введите место вашего обслуживания, учтите, что официальные дилеры сами добавляют записи о ремонтах автомобилей'")
        await state.set_state(PutHistoryStates.waiting_for_official)
    elif callback.data[:5] == "learn":
        allbuttons = []
        save_about_order=get_order(callback.data[5:])[0]
        allbuttons.append([types.InlineKeyboardButton(text="История", callback_data=f"history{save_about_order[5]}")])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=allbuttons)
        await callback.message.answer(f"*Дилер* - {save_about_order[0]}\n*Тип* - {save_about_order[1]}\n*Комментарий* - {save_about_order[2]}\n*Пробег* - {save_about_order[3]}\n*Дата* - {save_about_order[4]}", parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
    elif callback.data[:7]=="history":
        allbuttons = []
        history=get_history(callback.data[7:])
        for i in history:
            allbuttons.append([types.InlineKeyboardButton(text=f"{i[1]} {i[2]}", callback_data=f"learn{i[0]}")]) ##############################################################
        buttons_low=[types.InlineKeyboardButton(text="Информация", callback_data=f"getcarinfo{callback.data[7:]}"), types.InlineKeyboardButton(text="Добавить запись", callback_data=f"puthistory{callback.data[7:]}")]
        allbuttons.append(buttons_low)
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=allbuttons)
        await callback.message.delete()
        await callback.message.answer(f"*{callback.data[7:]}*\n\n*История Обслуживания:*\n\n", parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
    elif callback.data[:10]=="getcarinfo":
        car_info=get_car_information(callback.data[10:])
        buttons = []
        buttons.append(types.InlineKeyboardButton(text="В гараж", callback_data="garage"))
        buttons.append(types.InlineKeyboardButton(text="История", callback_data=f"history{car_info[1]}"))
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])
        await callback.message.delete()
        await callback.message.answer(f"*{car_info[1]}*\n\n*Инфорация об автомобиле:*\n\nБренд: *{car_info[3]}*\nМодель: *{car_info[4]}*\nЦвет: *{car_info[8]}*\nКомплектация: *{car_info[6]}*\nГод выпуска: *{car_info[5]}*\nДилер: *{car_info[7]}*", parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)

@dp.message(PutHistoryStates.waiting_for_official)
async def puthistory_place(message: types.Message, state: FSMContext):
    place=message.text
    plate=server[message.chat.id]
    puthistory_place_db(plate, place)
    kb = []
    listofworks = ["Техническое обслуживание", "Замена деталей", "Диагностика", "Дополнительные услуги"]
    for i in listofworks:
        kb.append(types.KeyboardButton(text=i))
    kb = [kb]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f"Выберите тип обслуживания", reply_markup=keyboard)
    await state.set_state(PutHistoryStates.waiting_for_type)  # Ключевой момент!

@dp.message(PutHistoryStates.waiting_for_type)
async def puthistory_type(message: types.Message, state: FSMContext):
    type=message.text
    plate = server[message.chat.id]
    puthistory_type_db(type, plate)
    await message.answer(f"Введите комментарий")#, reply_markup=keyboard)
    await state.set_state(PutHistoryStates.waiting_for_comment)  # Ключевой момент!

@dp.message(PutHistoryStates.waiting_for_comment)
async def puthistory_comment(message: types.Message, state: FSMContext):
    comment=message.text
    plate = server[message.chat.id]
    puthistory_comment_db(comment, plate)
    await message.answer(f"Введите пробег")#, reply_markup=keyboard)
    await state.set_state(PutHistoryStates.waiting_for_mileage)  # Ключевой момент!

@dp.message(PutHistoryStates.waiting_for_mileage)
async def puthistory_mileage(message: types.Message, state: FSMContext):
    mileage=message.text
    plate = server[message.chat.id]
    date=datetime.date.today()
    puthistory_mileage_db(mileage, date, plate)
    havetodelete = await message.answer(f"Запись создана!")#, reply_markup=keyboard)
    await state.clear()
    allbuttons = []
    history = get_history(plate)
    for i in history:
        allbuttons.append([types.InlineKeyboardButton(text=f"{i[1]} {i[2]}",
                                                      callback_data=f"learn{i[0]}")])  ##############################################################
    buttons_low = [types.InlineKeyboardButton(text="Информация", callback_data=f"getcarinfo{plate}"),
                   types.InlineKeyboardButton(text="Добавить запись", callback_data=f"puthistory{plate}")]
    allbuttons.append(buttons_low)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=allbuttons)
    time.sleep(5)
    await havetodelete.delete()
    await message.answer(f"*{plate}*\n\n*История Обслуживания:*\n\n",parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)



@dp.message(Command("garage"))
async def garage(message: types.Message, state):
    delete_every_unfinished(message.chat.id)
    await state.clear()
    if check_registration(message.chat.id)==0:
        await message.delete()
        await message.answer(f"Зарегистрируйтесь с помощью команды /registration, чтобы продолжить!")  # , reply_markup=keyboard)
    else:
        count_of_cars=get_cars(message.chat.id)
        if len(count_of_cars)==0:
            await message.answer(f"Вы пока не добавили автомобили,но вы можете сделать это с помощью команды /registrationcar")  # , reply_markup=keyboard)
        else:
            buttons = []
            for i in count_of_cars:
                buttons.append(types.InlineKeyboardButton(text=i[1], callback_data=f"getcarinfo{i[1]}"))
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])
            await message.delete()
            await message.answer(f"Выберите нужный автомобиль:\n/registrationcar - зарегистрировать новый автомобиль", reply_markup=keyboard)

@dp.message(Command("registrationcar"))
async def registrationcar_plate(message: types.Message, state: FSMContext):
    delete_every_unfinished(message.chat.id)
    await message.answer(f"Введите государственный регистрационный номер автомобиля")#, reply_markup=keyboard)
    await state.set_state(RegistrationCarStates.waiting_for_plate)  # Ключевой момент!

@dp.message(RegistrationCarStates.waiting_for_plate)
async def registrationcar_vin(message: types.Message, state: FSMContext):
    plate=message.text
    registrationcar_plate_db(message.chat.id, plate)
    await message.answer(f"Введите vin-номер автомобиля")#, reply_markup=keyboard)
    await state.set_state(RegistrationCarStates.waiting_for_vin)  # Ключевой момент!

@dp.message(RegistrationCarStates.waiting_for_vin)
async def registrationcar_brand(message: types.Message, state: FSMContext):
    vin=message.text
    registrationcar_vin_db(message.chat.id, vin)
    await message.answer(f"Введите или выберите бренд автомобиля")#, reply_markup=keyboard)
    await state.set_state(RegistrationCarStates.waiting_for_brand)  # Ключевой момент!

@dp.message(RegistrationCarStates.waiting_for_brand)
async def registrationcar_model(message: types.Message, state: FSMContext):
    brand=message.text
    registrationcar_brand_db(message.chat.id, brand)
    await message.answer(f"Введите модель автомобиля")#, reply_markup=keyboard)
    await state.set_state(RegistrationCarStates.waiting_for_model)  # Ключевой момент!

@dp.message(RegistrationCarStates.waiting_for_model)
async def registrationcar_year(message: types.Message, state: FSMContext):
    model=message.text
    registrationcar_model_db(message.chat.id, model)
    await message.answer(f"Введите год выпуска автомобиля")#, reply_markup=keyboard)
    await state.set_state(RegistrationCarStates.waiting_for_year)  # Ключевой момент!

@dp.message(RegistrationCarStates.waiting_for_year)
async def registrationcar_config(message: types.Message, state: FSMContext):
    year=message.text
    registrationcar_year_db(message.chat.id, year)
    await message.answer(f"Введите комплектацию автомобиля")#, reply_markup=keyboard)
    await state.set_state(RegistrationCarStates.waiting_for_config)  # Ключевой момент!

@dp.message(RegistrationCarStates.waiting_for_config)
async def registrationcar_dealer(message: types.Message, state: FSMContext):
    config=message.text
    registrationcar_config_db(message.chat.id, config)
    kb = []
    listofdealers = get_all_dealers()
    for i in listofdealers:
        kb.append(types.KeyboardButton(text=i[0]))
    kb = [kb]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f"Введите или выберите дилера автомобиля" ,reply_markup=keyboard)#, reply_markup=keyboard)
    await state.set_state(RegistrationCarStates.waiting_for_dealer)  # Ключевой момент!

@dp.message(RegistrationCarStates.waiting_for_dealer)
async def registrationcar_color(message: types.Message, state: FSMContext):
    dealer=message.text
    registrationcar_dealer_db(message.chat.id, dealer)
    car_colors = [
        "Белый", "Чёрный", "Серебристый", "Серый",
        "Синий", "Тёмно-синий", "Красный", "Бордовый",
        "Зелёный", "Хаки", "Бежевый", "Голубой",
        "Графитовый", "Оранжевый", "Жёлтый", "Фиолетовый",
        "Золотистый", "Перламутровый", "Коричневый", "Бирюзовый"
    ]
    kb = []
    for i in car_colors:
        kb.append([types.KeyboardButton(text=i)])
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
    await message.answer(f"Введите или выберите цвет автомобиля", reply_markup=keyboard)
    await state.set_state(RegistrationCarStates.waiting_for_color)  # Ключевой момент!

@dp.message(RegistrationCarStates.waiting_for_color)
async def registrationcar_successfully(message: types.Message, state: FSMContext):
    color=message.text
    registrationcar_color_db(message.chat.id, color)
    await message.answer(f"Вы успешно зарегистрировали автомобиль!")#, reply_markup=keyboard)
    await state.clear()  # Ключевой момент!


@dp.message(Command("registration"))
async def registration_number(message: types.Message, state: FSMContext):
    if check_registration(message.chat.id)==0:
        await message.answer(f"Зарегистрируйтесь с помощью вашего номера телефона!", reply_markup=phone.contact_keyboard())
        await state.set_state(RegistrationStates.waiting_for_phone)  # Ключевой момент!
    else:
        await message.answer(f"Вы уже зарегистрированы!")

@dp.message(RegistrationStates.waiting_for_phone)
async def registration_name(message: types.Message, state: FSMContext):
    number=(message.contact.phone_number)
    registration_phone(message.chat.id, number)
    await message.answer("Введите ваше имя!")
    await state.set_state(RegistrationStates.waiting_for_name)  # Ключевой момент!

@dp.message(RegistrationStates.waiting_for_name)
async def registration_successfully(message: types.Message, state: FSMContext):
    name=message.text
    registration_name(message.chat.id, name)
    await message.answer("Вы успешно зарегистрированы!")
    await state.clear() # Ключевой момент!

# Запуск процесса пуллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    over()
    print("Программа завершена!")
