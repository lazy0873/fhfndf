

import os
import random
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from flask import Flask

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear la aplicación Flask
app = Flask(__name__)

# Token del bot
TOKEN = os.getenv('8556431265:AAFZA51BdMbGdAsqpDu7BlNNu4lzpAyy8JM')  # Asegúrate de que esta variable esté configurada en Render

# Inicializar Updater y Dispatcher para el bot
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Preguntas motivacionales variadas para enviar a lo largo de los días
motivational_questions = [
    "¿Ya desayunaste hoy? ¿Listo para empezar con energía?",
    "¿Comiste algo saludable? ¡Recuerda que el cuerpo es tu templo!",
    "¿Cómo te sientes hoy? ¡Hoy es un buen día para superar tus límites!",
    "¿Ya entrenaste hoy? ¡Recuerda que cada pequeño paso te acerca a tu meta!",
    "¿Te has hidratado? ¡El agua es clave para mantenerte al 100%!",
    "¿Qué metas tienes hoy? ¡Vamos a alcanzarlas juntos!",
    "¿Ya has movido tu cuerpo? ¡El entrenamiento es la clave del éxito!",
    "¿Te has estirado hoy? ¡No olvides cuidar tus músculos!"
]

# Frases motivacionales
motivational_quotes = [
    "¡Hoy es un gran día para ser mejor que ayer!",
    "El dolor de hoy es la fuerza de mañana.",
    "Cada día es una nueva oportunidad para mejorar.",
    "La constancia es la clave del éxito. ¡No te rindas!",
    "Lo mejor está por venir, sigue adelante.",
    "Un pequeño paso cada día, ¡y pronto estarás en la cima!",
    "Recuerda que la motivación se construye con acción. ¡Sigue adelante!"
]

# Mensaje de bienvenida
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "¡Hola! Soy tu asistente personal CoreX. Estoy aquí para motivarte todos los días y ayudarte a alcanzar tus metas. 💪"
    )
    send_motivational_question(update)

# Comando /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "¡Estoy aquí para ayudarte! Solo responde a las preguntas diarias y siempre te motivaré a dar lo mejor de ti. 💥"
    )

# Función para enviar una pregunta motivacional
def send_motivational_question(update: Update) -> None:
    question = random.choice(motivational_questions)
    update.message.reply_text(question)

# Función para manejar las respuestas de los usuarios
def handle_response(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()

    # Si el usuario responde negativamente
    if "no" in user_message or "no lo he hecho" in user_message:
        motivational_reply = random.choice([
            "No te preocupes, ¡todos tenemos días difíciles! Lo importante es que sigas adelante. 💪",
            "¡No pasa nada! Mañana será un nuevo día para comenzar con más fuerza. ¡Tú puedes!",
            "¡Ánimo! Cada día es una oportunidad para mejorar. ¡Tú eres más fuerte de lo que crees!"
        ])
    else:
        motivational_reply = random.choice([
            "¡Excelente! Sigue así, ¡estás en el camino correcto! 🌟",
            "¡Muy bien! Cada paso te acerca más a tu meta. ¡Vamos con todo!",
            "¡Fantástico! Recuerda que la constancia es la clave. ¡Sigue trabajando duro!"
        ])

    update.message.reply_text(motivational_reply)
    send_motivational_question(update)  # Después de cada respuesta, manda una nueva pregunta

# Función principal para iniciar el bot con polling
def main():
    # Agregar manejadores de comandos
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Agregar un manejador para las respuestas
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_response))

    # Iniciar polling para escuchar los mensajes
    updater.start_polling()
    updater.idle()  # Mantiene el bot funcionando

# Configurar Flask para que funcione con Render
@app.route('/')
def home():
    return "El bot está funcionando correctamente!"

if __name__ == '__main__':
    # Inicia el bot y la aplicación Flask
    main()
    app.run(debug=True, port=5000)
