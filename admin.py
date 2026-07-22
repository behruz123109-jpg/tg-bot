from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiosqlite
from database import DB_NAME

router = Router()

# Admin ekanligini tekshiruvchi filtr (Sizning ID'ingiz)
ADMIN_IDS = [123456789] # main.py dagi ID bilan bir xil bo'lishi kerak

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# FSM holatlari (Matnni tahrirlash uchun)
class AdminStates(StatesGroup):
    waiting_for_new_start_text = State()
    waiting_for_broadcast_message = State()

@router.message(F.text == "👑 Admin Panel")
async def admin_panel_handler(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📊 Statistika"), types.KeyboardButton(text="💸 To'lovlar So'rovi")],
            [types.KeyboardButton(text="✏️ Start Matnini O'zgartirish"), types.KeyboardButton(text="🛠 Tanaffus Rejimi")],
            [types.KeyboardButton(text="⬅️ Asosiy Menyu")]
        ],
        resize_keyboard=True
    )
    await message.answer("👑 **TapMasterBot Admin Paneliga xush kelibsiz!**\nKerakli bo'limni tanlang:", reply_markup=keyboard)

@router.message(F.text == "📊 Statistika")
async def admin_stats(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            total_users = (await cursor.fetchone())[0]
            
        async with db.execute("SELECT COUNT(*) FROM payouts WHERE status = 'pending'") as cursor:
            pending_payouts = (await cursor.fetchone())[0]

    stats_text = (
        f"📊 <b>TapMasterBot Statistikasi:</b>\n\n"
        f"👥 Jami o'yinchilar: <b>{total_users} ta</b>\n"
        f"⏳ Kutilayotgan to'lovlar: <b>{pending_payouts} ta</b>\n"
        f"🟢 Holat: <b>Ishlamoqda (Online)</b>"
    )
    await message.answer(stats_text)

@router.message(F.text == "✏️ Start Matnini O'zgartirish")
async def change_start_text_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    await state.set_state(AdminStates.waiting_for_new_start_text)
    await message.answer("✍️ Iltimos, foydalanuvchilar uchun yangi **Start matnini** yuboring (HTML format qo'llab-quvvatlanadi):")

@router.message(AdminStates.waiting_for_new_start_text)
async def save_new_start_text(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
        
    new_text = message.text
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE settings SET setting_value = ? WHERE setting_key = 'start_text'", 
            (new_text,)
        )
        await db.commit()
        
    await state.clear()
    await message.answer("✅ **Start matni muvaffaqiyatli yangilandi!** Botni qayta yoqish shart emas, darhol kuchga kirdi.")

@router.message(F.text == "⬅️ Asosiy Menyu")
async def back_to_main(message: types.Message):
    from keyboards import get_main_menu
    await message.answer("Asosiy menyuga qaytdingiz:", reply_markup=get_main_menu(is_admin(message.from_user.id)))
