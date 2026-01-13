import asyncio
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # Mostrar logs en la consola
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# Habilitar logging detallado para aiogram
logging.getLogger('aiogram').setLevel(logging.INFO)
logging.getLogger('asyncio').setLevel(logging.INFO)

# Importar el bot
from app.bot import start_bot

# Variable global para la tarea del bot
bot_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación"""
    global bot_task
    
    # Iniciar el bot en segundo plano
    bot_task = asyncio.create_task(start_bot())
    logger.info("✅ Aplicación iniciada")
    
    yield
    
    # Detener el bot al cerrar la aplicación
    if bot_task:
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            pass
    logger.info("❌ Aplicación detenida")

# Crear la aplicación FastAPI
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    """Ruta raíz para verificar que el servidor está funcionando"""
    return {
        "status": "running",
        "service": "Medixio AI Bot",
        "version": "0.1.0"
    }

# Bloque principal para ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    
    # Iniciar la aplicación FastAPI
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
