from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from config import ADMIN_IDS

class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        # Agar foydalanuvchi adminlar ro'yxatida bo'lmasa, so'rovni to'xtatish
        if event.from_user.id not in ADMIN_IDS:
            return
            
        return await handler(event, data)
