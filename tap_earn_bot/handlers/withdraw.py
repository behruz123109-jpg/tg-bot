from aiogram import Router, F
from aiogram.types import Message
from database.queries import get_user, get_setting

router = Router()

@router.message(F.text == "💸 Yechib olish")
async def withdraw_request(message: Message):
    user = await get_user(message.from_user.id)
    min_withdraw = int(await get_setting("min_withdraw_diamonds"))
    
    if user:
        if user["diamonds"] >= min_withdraw:
            await message.answer(
                f"Sizda {user['diamonds']} ta Olmos bor. Yechib olish uchun kartangiz yoki PUBG ID raqamingizni kiriting."
            )
            # Bu yerda FSM (Finite State Machine) orqali ma'lumotlarni qabul qilish davom ettiriladi
        else:
            await message.answer(
                f"❌ Yechib olish uchun minimal miqdor: {min_withdraw} Olmos.\n"
                f"Sizda hozircha: {user['diamonds']} Olmos bor."
            )
