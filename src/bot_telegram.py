import os
import sys
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Agregar path raiz
sys.path.append(os.getcwd())
from src.agente import analizar_riesgo

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
# Cloud Run nos pasara el puerto en esta variable
PORT = int(os.environ.get("PORT", "8443"))
# Esta variable determinara si usamos Webhook (Nube) o Polling (Local)
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 

if not TOKEN:
    raise ValueError("Error critico: Falta el TOKEN en .env")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    modo_operacion = "NUBE (Webhook)" if WEBHOOK_URL else "LOCAL (Polling)"
    
    await update.message.reply_text(
        f"SISTEMA SENTINELA\n"
        f"Usuario: {user.first_name}\n"
        f"Estado: OPERATIVO\n"
        f"Modo: {modo_operacion}\n\n"
        f"Instrucciones: Ingrese el nombre de la zona a consultar."
    )

async def procesar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lugar = update.message.text
    chat_id = update.message.chat_id
    
    # Feedback operativo simple
    msg_espera = await update.message.reply_text(f"Iniciando analisis de inteligencia para: {lugar}...")
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    
    try:
        loop = asyncio.get_event_loop()
        reporte = await loop.run_in_executor(None, analizar_riesgo, lugar)
        await update.message.reply_text(reporte)
    except Exception as e:
        await update.message.reply_text(f"ERROR DEL SISTEMA: {e}")
    finally:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_espera.message_id)
        except:
            pass

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_mensaje))

    # --- LOGICA HIBRIDA ---
    if WEBHOOK_URL:
        print(f"SISTEMA INICIADO EN MODO WEBHOOK (Puerto {PORT})")
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
        )
    else:
        print("SISTEMA INICIADO EN MODO POLLING (Local)")
        application.run_polling()

if __name__ == "__main__":
    main()