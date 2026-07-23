from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from config import ADMIN_IDS

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    # Dastlabki sodda tekshiruv, garchi middleware bo'lsa ham xavfsizlik uchun
    if message.from_user.id not in ADMIN_IDS:
        return
        
    await message.answer(
        "👨‍💻 **Admin Panelga Xush Kelibsiz!**\n\n"
        "Bu yerdan bot sozlamalarini va foydalanuvchilar statistikasini ko'rishingiz mumkin. "
        "(Kelajakda tugmalar qo'shiladi)",
        parse_mode="Markdown"
    )

# Adminlarga userlar statistikasini ko'rish funksiyasi
@router.message(Command("stats"))
async def bot_stats(message: Message):
    if message.from_user.id in ADMIN_IDS:
        # Bu yerda DB dan jami foydalanuvchilarni sanab chiqaruvchi so'rov yoziladi
        await message.answer("📊 Bot statistikasi tez orada ulanadi.")
