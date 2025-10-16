import os
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile

from logger import log_action
from tugmachalar import *

router = Router()


class Buyurtmalar(StatesGroup):
    name = State()
    address = State()
    phone = State()
    payment = State()


# HELP komandasi
@router.message(Command("help"))
async def cmd_help_command(message: Message):
    log_action(message.from_user, "/help komandasi bosildi")
    await message.answer("ℹ️ Agar yordam kerak bo‘lsa: @shakh_wu")


# CATALOG komandasi
@router.message(Command("catalog"))
async def cmd_catalog_command(message: Message):
    log_action(message.from_user, "/catalog komandasi bosildi")
    await message.answer("🍰 Tortlardan birini tanlang:", reply_markup=inline_katalog)


# CATALOG tugmasi
@router.callback_query(F.data == "catalog")
async def cmd_catalog(callback: CallbackQuery):
    log_action(callback.from_user, "Katalog tugmasi bosildi")
    await callback.message.edit_text("🍰 Tortlardan birini tanlang:", reply_markup=inline_katalog)


# HELP tugmasi
@router.callback_query(F.data == "help")
async def cmd_help(callback: CallbackQuery):
    log_action(callback.from_user, "Yordam tugmasi bosildi")
    await callback.message.edit_text("ℹ️ Agar yordam kerak bo‘lsa: @shakh_wu", reply_markup=menyu)


# Ortga (asosiy menyu)
@router.callback_query(F.data == "back_main")
async def cmd_back_main(callback: CallbackQuery):
    log_action(callback.from_user, "Ortga (asosiy menyu) tugmasi bosildi")
    await callback.message.edit_text("🏠 Asosiy menyuga qaytdik", reply_markup=menyu)




# Tortlarni tanlash
@router.callback_query(F.data == "kremli_tort")
async def cmd_kremli_tort(callback: CallbackQuery):
    log_action(callback.from_user, "Kremli tort tanlandi")
    image1 = FSInputFile("rasmlar/kremli.jpg")
    await callback.message.delete()
    await callback.message.answer_photo(photo=image1, caption="🧁 Kremli tort - 120.000 so‘m", reply_markup=buyurtma)


@router.callback_query(F.data == "mevali_tort")
async def cmd_mevali_tort(callback: CallbackQuery):
    log_action(callback.from_user, "Mevali tort tanlandi")
    image2 = FSInputFile("rasmlar/mevali.jpg")
    await callback.message.answer_photo(photo=image2, caption="🍓 Mevali tort - 150.000 so‘m", reply_markup=buyurtma)


@router.callback_query(F.data == "shokoladli_tort")
async def cmd_shokoladli(callback: CallbackQuery):
    log_action(callback.from_user, "Shokoladli tort tanlandi")
    image3 = FSInputFile("rasmlar/shkaladli.jpg")
    await callback.message.answer_photo(photo=image3, caption="🍫 Shokoladli tort - 200.000 so‘m", reply_markup=buyurtma)


@router.callback_query(F.data == "muzqaymoq_tort")
async def cmd_muzqaymoq(callback: CallbackQuery):
    log_action(callback.from_user, "Muzqaymoqli tort tanlandi")
    image4 = FSInputFile("rasmlar/muzqaymoqli.jpg")
    await callback.message.answer_photo(photo=image4, caption="🍦 Muzqaymoqli tort - 150.000 so‘m", reply_markup=buyurtma)


@router.callback_query(F.data == "standart_tort")
async def cmd_standart(callback: CallbackQuery):
    log_action(callback.from_user, "Standart tort tanlandi")
    image5 = FSInputFile("rasmlar/standart.jpg")
    await callback.message.answer_photo(photo=image5, caption="🎂 Standart bazm torti - 100.000 so‘m", reply_markup=buyurtma)


@router.callback_query(F.data == "protainli_tort")
async def cmd_protain(callback: CallbackQuery):
    log_action(callback.from_user, "Protainli tort tanlandi")
    image6 = FSInputFile("rasmlar/protainli.jpg")
    await callback.message.answer_photo(photo=image6, caption="💪 Protainli tort - 250.000 so‘m", reply_markup=buyurtma)


# Ortga (katalog)
@router.callback_query(F.data == "back_catalog")
async def cmd_back_catalog(callback: CallbackQuery):
    log_action(callback.from_user, "Ortga (katalog) tugmasi bosildi")
    await callback.message.answer("🍰 Tortlardan birini tanlang:", reply_markup=inline_katalog)


# Buyurtma jarayoni – ism
@router.callback_query(F.data == "buyurtma")
async def cmd_buyurtma(callback: CallbackQuery, state: FSMContext):
    log_action(callback.from_user, "Buyurtma jarayoni boshlandi")
    await state.set_state(Buyurtmalar.name)
    await callback.message.answer("👤 Ismingizni kiriting:")


@router.message(Buyurtmalar.name)
async def buyurtma_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    log_action(message.from_user, f"Ism kiritildi: {message.text}")
    await state.set_state(Buyurtmalar.address)
    await message.answer("📍 Manzilingizni kiriting:")


@router.message(Buyurtmalar.address)
async def buyurtma_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    log_action(message.from_user, f"Manzil kiritildi: {message.text}")
    await state.set_state(Buyurtmalar.phone)
    await message.answer("📞 Telefon raqamingizni kiriting:", reply_markup=phone_number)


@router.message(Buyurtmalar.phone)
async def buyurtma_phone(message: Message, state: FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

    await state.update_data(phone=phone_number)
    log_action(message.from_user, f"Telefon raqam kiritildi: {phone_number}")

    await state.set_state(Buyurtmalar.payment)
    await message.answer("💰 To‘lov usulini tanlang:", reply_markup=tolov_qilish)




# To‘lov usullari
@router.callback_query(F.data == "online_pay")
async def process_payment_online(callback: CallbackQuery, state: FSMContext):
    payment_text = "online"
    await state.update_data(payment=payment_text)

    await callback.message.answer(
        "Karta raqami: 9860 1234 5678 9012 ga online tolov va chek @shakh_wu ga :)"
    )

    data = await state.get_data()
    log_action(callback.from_user, f"To‘lov usuli tanlandi: {payment_text}")

    order_text = (
        f"✅ Buyurtma qabul qilindi!\n\n"
        f"👤 Ism: {data['name']}\n"
        f"📍 Manzil: {data['address']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"💰 To‘lov: {data['payment']}"
    )

    await callback.message.answer(order_text, reply_markup=menyu)
    await state.clear()
    await callback.answer("Buyurtma tugallandi ✅", show_alert=True)


@router.callback_query(F.data == "cash")
async def process_payment_cash(callback: CallbackQuery, state: FSMContext):
    payment_text = "cash"
    await state.update_data(payment=payment_text)

    await callback.message.answer(
        "Buyurtma manzilingizga yetkazilgandan keyin to‘laysiz :)"
    )

    data = await state.get_data()
    log_action(callback.from_user, f"To‘lov usuli tanlandi: {payment_text}")

    order_text = (
        f"✅ Buyurtma qabul qilindi!\n\n"
        f"👤 Ism: {data['name']}\n"
        f"📍 Manzil: {data['address']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"💰 To‘lov: {data['payment']}"
    )

    await callback.message.answer(order_text, reply_markup=menyu)
    await state.clear()
    await callback.answer("Buyurtma tugallandi ✅", show_alert=True)


















# Har qanday matnli xabarni oddiy loglash (jsonsiz)
@router.message(F.text)
async def handle_text_message(message: Message):
    log_action(message.from_user, "Matnli xabar yuborildi")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_id = message.from_user.id
    full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
    text = message.text

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_line = f"{now} | USER_ID:{user_id} | NAME:{full_name} | TEXT:{text}\n"

    with open(os.path.join(logs_dir, "text_messages.log"), "a", encoding="utf-8") as logf:
        logf.write(log_line)

    await message.answer("✅ Sizning xabaringiz qabul qilindi!")
