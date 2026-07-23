from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject
from database.queries import add_user, get_user, get_setting
from keyboards.default_kbd import main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    referrer_id = None
    if command.args and command.args.isdigit():
        possible_referrer = int(command.args)
        if possible_referrer != message.from_user.id:
            referrer_id = possible_referrer

    await add_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username,
        referrer_id=referrer_id
    )

    start_text = await get_setting("start_text")
    await message.answer(start_text, reply_markup=main_menu())

@router.message(F.text == "💎 Balans va Hamyon")
async def show_balance(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        text = (
            f"👤 **Foydalanuvchi:** {user['full_name']}\n\n"
            f"🪙 **Tangalar:** {user['coins']}\n"
            f"💎 **Olmoslar:** {user['diamonds']}\n"
            f"⚡ **Energiyangiz:** {user['energy']}/{user['max_energy']}"
        )
        await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "ℹ️ Yordam")
async def show_help(message: Message):
    help_text = await get_setting("help_text")
    await message.answer(help_text)
