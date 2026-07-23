from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.queries import process_tap, get_user
from keyboards.inline_kbd import tap_keyboard

router = Router()

@router.message(F.text == "⚡ Tap (Tanga yig'ish)")
async def open_tap_menu(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(
            "Tangalarni yig'ish uchun quyidagi tugmani bosing:",
            reply_markup=tap_keyboard(user["coins"], user["energy"])
        )

@router.callback_query(F.data == "do_tap")
async def handle_tap(callback: CallbackQuery):
    success, coins, energy = await process_tap(callback.from_user.id)
    if success:
        await callback.message.edit_reply_markup(
            reply_markup=tap_keyboard(coins, energy)
        )
        await callback.answer("+1 Tanga!", show_alert=False)
    else:
        await callback.answer("Energiyangiz tugadi! Biroz kuting.", show_alert=True)

@router.callback_query(F.data == "refresh_tap")
async def handle_refresh(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    if user:
        await callback.message.edit_reply_markup(
            reply_markup=tap_keyboard(user["coins"], user["energy"])
        )
        await callback.answer("Yangilandi!")
