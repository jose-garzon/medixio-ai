from aiogram import F, Router
from aiogram.types import Message

# Crear router para mensajes
message_router = Router()

@message_router.message(F.text)
async def handle_text_message(message: Message):
    """Manejador para mensajes de texto"""
    # Aquí puedes agregar lógica para procesar el mensaje
    response = (
        f"📝 He recibido tu mensaje:\n\n"
        f"*{message.text}*\n\n"
        "¿En qué más puedo ayudarte?"
    )
    await message.answer(response, parse_mode="Markdown")
