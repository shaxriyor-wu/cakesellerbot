import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery

from logger import log_action, log_system
import traceback
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from config import TOKEN
from tugmachalar import *


bot = Bot(token=TOKEN)
dp = Dispatcher()

class buyurtmalar(StatesGroup):
    name = State()
    address = State()
    phone = State()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    log_action(message.from_user, "/start komandasi bosildi")
    await message.answer(f"Assalomu alaykum hurmatli foydalanuvchi, bizning To'rt sotish boyicha botimizga xush kelibsiz!", reply_markup=menyu)


@dp.callback_query(F.data == "catalog")
async def cmd_catalog(callback: CallbackQuery):
    log_action(callback.from_user, "Katalog tugmasi bosildi")
    await callback.message.edit_text("tortlardan birini tanlang:", reply_markup=inline_katalog)

@dp.callback_query(F.data == "back")
async def cmd_back(callback: CallbackQuery):
    log_action(callback.from_user, "Ortga tugmasi bosildi")
    await callback.message.edit_text("Katalogga qaytdik", reply_markup=menyu)

@dp.callback_query(F.data == "help")
async def cmd_help(callback: CallbackQuery):
    log_action(callback.from_user, "Yordam tugmasi bosildi")
    await callback.message.edit_text(f"Agar sizga qandaydir yordam kerak bolsa @shakh_wu ga boglaning", reply_markup=menyu)

@dp.callback_query(F.data == "kremli_tort")
async def cmd_kremli_tort(callback: CallbackQuery):
    phot = FSInputFile("images/kremli.jpg")
    await callback.message.answer_photo(photo=phot, caption=f"Kremli tort tanlandi!\n Bu tortning narxi 120.000 so'm\n", reply_markup=buyurtma)
    log_action(callback.from_user, "Kremli tort tanlandi")

@dp.callback_query(F.data == "mevali_tort")
async def cmd_mevali_tort(callback: CallbackQuery):
    log_action(callback.from_user, "Mevali tort tanlandi")
    await callback.message.edit_text(f"Mevali tort tanlandi!\n Bu tortning narxi 150.000 so'm\n", reply_markup=buyurtma)

@dp.callback_query(F.data == "shokoladli")
async def cmd_shokoladli(callback: CallbackQuery):
    log_action(callback.from_user, "Shokoladli tort tanlandi")
    await callback.message.edit_text(f"Shokoladli tort tanlandi!\n Bu tortning narxi 160.000 so'm\n", reply_markup=buyurtma)

@dp.callback_query(F.data == "muzqaymoq_tort")
async def cmd_muzqaymoq_tort(callback: CallbackQuery):
    log_action(callback.from_user, "Muzqaymoqli tort tanlandi")
    await callback.message.edit_text(f"Muzqaymoqli tort tanlandi!\n Bu tortning narxi 150.000 so'm\n", reply_markup=buyurtma)

@dp.callback_query(F.data == "standart")
async def cmd_standart(callback: CallbackQuery):
    log_action(callback.from_user, "Standart bazm torti tanlandi")
    await callback.message.edit_text(f"Standart bazm torti tanlandi!\n Bu tortning narxi 100.000 so'm\n", reply_markup=buyurtma)

@dp.callback_query(F.data == "protain")
async def cmd_protain(callback: CallbackQuery):
    log_action(callback.from_user, "Protainli tort tanlandi")
    await callback.message.edit_text(f"Protainli tort tanlandi!\n Bu tortning narxi 250.000 so'm\n", reply_markup=buyurtma)



@dp.callback_query(F.data == "buyurtma")
async def cmd_buyurtma(callback: CallbackQuery, state: FSMContext):
    await state.set_state(buyurtmalar.name)
    await callback.message.answer("Ismingizni kiriting:")

@dp.message(buyurtmalar.name)
async def buyurtma_2(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(buyurtmalar.address)
    await message.answer("Manzilingizni kiriting:")

@dp.message(buyurtmalar.address)
async def buyurtma_3(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(buyurtmalar.phone)
    await message.answer("Telefon raqamingizni kiriting:", reply_markup=phone_number)
@dp.message(buyurtmalar.phone, F.contact)
async def buyurtma_4(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()
    name = data.get("name")
    address = data.get("address")
    phone = data.get("phone")
    await message.answer(f"Buyurtmangiz qabul qilindi!\nIsm: {name}\nManzil: {address}\nTelefon raqam: {phone}", reply_markup=royxatdan_keyingi_menyu)
    await state.clear()

@dp.callback_query(F.data == "pay")
async def cmd_pay(callback: CallbackQuery):
    log_action(callback.from_user, "To'lov tugmasi bosildi")
    await callback.message.edit_text(f"Hozircha bizda bizda online tolov tizimi mavjjud emas. Buyurtma narxini Buyurtmani olganingizdan keyin tolashingiz mumkin", reply_markup=malumot)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

