import os
import sys
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Agregar path raiz
sys.path.append(os.getcwd())

# Importamos tu cerebro
from src.agente import analizar_riesgo

# Cargar variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("Error: Token de Telegram no encontrado en .env")

# --- FUNCIONES DEL BOT ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # Bienvenida seria y minimalista
    await update.message.reply_text(
        f"SISTEMA SENTINELA\nUsuario: {user.first_name}\n\nEscriba la zona o ciudad a consultar."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Instrucciones: Ingrese solo el nombre del lugar (ej: Naucalpan, Mazatlan).")

async def procesar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lugar = update.message.text
    chat_id = update.message.chat_id
    
    # Feedback operativo simple
    msg_espera = await update.message.reply_text(f"Procesando solicitud para: {lugar}...")
    
    # Estado 'Escribiendo'
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    
    try:
        # Ejecutar analisis en hilo separado
        loop = asyncio.get_event_loop()
        reporte = await loop.run_in_executor(None, analizar_riesgo, lugar)
        
        # Enviar reporte. Usamos Markdown simple para que se vea limpio pero estructurado.
        await update.message.reply_text(reporte)
        
    except Exception as e:
        await update.message.reply_text(f"Error critico: {e}")
    finally:
        # Limpieza de mensajes de estado
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_espera.message_id)
        except:
            pass

def main():
    print("Servicio de Bot iniciado. Esperando peticiones...")
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_mensaje))

    application.run_polling()

if __name__ == "__main__":
    main()