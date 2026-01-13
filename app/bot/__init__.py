import logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

# Configurar logger
logger = logging.getLogger(__name__)

# Importar configuración
from app.core.config import settings

# Inicializar el bot y el dispatcher
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

# Middleware para registrar mensajes
@dp.message.middleware()
async def log_messages(handler, event, data):
    """Middleware para registrar todos los mensajes recibidos"""
    message = event.event if hasattr(event, 'event') else event
    if hasattr(message, 'text') and message.text:
        user = message.from_user
        logger.info(f"📨 Mensaje recibido de {user.full_name} (@{user.username}): {message.text}")
    
    # Continuar con el siguiente middleware o manejador
    return await handler(event, data)

def setup_handlers():
    """Configurar los manejadores de mensajes y comandos"""
    from .handlers import commands, messages
    
    # Incluir routers
    dp.include_router(commands.command_router)
    dp.include_router(messages.message_router)
    
    logger.info("✅ Manejadores configurados")

async def start_bot():
    """Iniciar el bot"""
    try:
        # Configurar manejadores
        setup_handlers()
        
        # Información del bot
        me = await bot.get_me()
        logger.info(f"🤖 Bot iniciado como @{me.username} (ID: {me.id})")
        logger.info("📡 Escuchando mensajes... (Presiona Ctrl+C para salir)")
        
        # Iniciar el bot
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.error(f"❌ Error en el bot: {e}")
        raise
