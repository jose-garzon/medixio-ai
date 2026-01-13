from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

# Crear router para comandos
command_router = Router()

@command_router.message(CommandStart())
async def cmd_start(message: Message):
    """Manejador para el comando /start"""
    await message.answer(
        "👋 ¡Hola! Soy tu asistente médico virtual. "
        "Estoy aquí para ayudarte con tus consultas médicas.\n\n"
        "Usa /ayuda para ver los comandos disponibles."
    )

@command_router.message(Command("ayuda"))
async def cmd_help(message: Message):
    """Muestra los comandos disponibles"""
    help_text = (
        "🤖 *Comandos disponibles:*\n\n"
        "/start - Iniciar el bot\n"
        "/ayuda - Mostrar esta ayuda\n"
        "/cita - Programar una cita médica\n"
        "/medicamento - Consultar información de medicamentos"
    )
    await message.answer(help_text, parse_mode="Markdown")
