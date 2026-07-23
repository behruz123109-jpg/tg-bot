from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from database.queries import get_setting

class MaintenanceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        # Bazadan maintenance_mode statusini tekshirish
        maintenance = await get_setting("maintenance_mode")
        
        if maintenance.lower() == "true":
            await event.answer("⚠️ Botda texnik ta'mirlash ishlari olib borilmoqda. Iltimos, birozdan so'ng urinib ko'ring.")
            return
            
        return await handler(event, data)
