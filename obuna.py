import logging
from aiogram import Router, Bot, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from tugmachalar import menyu

router = Router()

# 🔑 Majburiy obuna bo‘lishi kerak bo‘lgan kanal
REQUIRED_CHANNELS = [
    "@shaxriyor_karimberdiyev",   # kanal username
]

# 🔑 Kanal nomlari
CHANNEL_NAMES = {
    "@shaxriyor_karimberdiyev": "📢 Shaxiy blog",
}


# 📌 Obunani tekshirish
async def check_user_subscription(user_id: int, bot: Bot) -> dict:
    not_subscribed = []

    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status == "left":  # obuna bo‘lmagan
                not_subscribed.append(channel)
        except Exception as e:
            logging.error(f"Kanal {channel} uchun xatolik: {e}")
            not_subscribed.append(channel)

    return {
        "is_subscribed": len(not_subscribed) == 0,
        "not_subscribed_channels": not_subscribed,
    }


# 📌 Inline tugmalar yaratish
def create_subscription_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for channel in REQUIRED_CHANNELS:
        channel_name = CHANNEL_NAMES.get(channel, channel)
        channel_link = f"https://t.me/{channel.replace('@', '')}"

        buttons.append([InlineKeyboardButton(
            text=f"🔗 {channel_name}",
            url=channel_link
        )])

    # Tekshirish tugmasi
    buttons.append([InlineKeyboardButton(
        text="✅ Obunani tekshirish",
        callback_data="check_subscription"
    )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# 📌 Start komandasi uchun
@router.message(F.text == "/start")
async def cmd_start(message: Message, bot: Bot):
    user_id = message.from_user.id
    subscription_status = await check_user_subscription(user_id, bot)

    if subscription_status["is_subscribed"]:
        await message.answer(
            f"👋 Salom, {message.from_user.full_name}!\n\n"
            "Siz **📢 Shaxiy blog** kanaliga obuna bo‘lgansiz ✅.\n\n"
            "Endi botdan foydalanishingiz mumkin 🚀", reply_markup=menyu
        )
    else:
        await message.answer(
            "❌ Botdan foydalanish uchun quyidagi kanalga obuna bo‘ling:",
            reply_markup=create_subscription_keyboard()
        )


# 📌 Callback orqali tekshirish
@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    subscription_status = await check_user_subscription(user_id, bot)

    if subscription_status["is_subscribed"]:
        await callback.message.edit_text(
            f"✅ Rahmat, {callback.from_user.full_name}!\n"
            "Siz **📢 Shaxiy blog** kanaliga obuna bo‘ldingiz.\n\n"
            "Endi botdan foydalanishingiz mumkin 🚀", reply_markup=menyu
        )
        await callback.answer("Obuna tasdiqlandi ✅")
    else:
        not_subscribed_names = []
        for channel in subscription_status["not_subscribed_channels"]:
            name = CHANNEL_NAMES.get(channel, channel)
            not_subscribed_names.append(f"❌ {name}")

        await callback.answer("Hali ham obuna bo‘lmagansiz!", show_alert=True)
        await callback.message.edit_text(
            "⚠️ Quyidagi kanalga obuna bo‘lmadingiz:\n\n" +
            "\n".join(not_subscribed_names) +
            "\n\nIltimos, obuna bo‘ling va qayta tekshiring.",
            reply_markup=create_subscription_keyboard()
        )
