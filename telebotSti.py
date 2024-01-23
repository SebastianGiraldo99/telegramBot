import requests.exceptions
import telebot
from telebot import types

TOKEN = '6746321824:AAGv0cFhzwdwmb5gFtz66LFVyJSJkqe3Gfw'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['empezar'])
def sendWelcomeMessage(message):
    bot.reply_to(message, 'Bienvenido al Bot STI')

@bot.message_handler(commands=['info'])
def infomationBot(message):
    bot.reply_to(message, 'Este es un bot creado para el envio masivo de mensajes')
    print(message.chat)

@bot.message_handler(commands=['vincular'])
def vinculation(message):
    bot.reply_to(message, 'Vinculado con exito')
    print(message.chat)

##Enviar mensajes a un grupo en especifico usando el nombre del grupo como identificador.
# @bot.message_handler(commands=['buenosDias'])
# def buenosDiasGrupo(message):
#     if message.chat.title == 'PruebaBot':
#         bot.reply_to(message, f"Este es un mensaje personalizado para el grupo {message.chat.title}")
#     else:
#         bot.reply_to(message, 'No es posible dar informacion en este grupo')
#     print(message.chat)


@bot.message_handler(commands=['saludar'])
def get_chat_id(message):
    chat_id = message.chat.id
    print(chat_id)
    # bot.send_message(chat_id, f"El ID del grupo es: {chat_id}")
    bot.send_message(message,"hola")

# ID_DEL_GRUPO = -1001977588535
# @bot.message_handler(commands=['enviar_grupo'])
# def enviar_mensaje_al_grupo(message):
#     mensaje = "¡Hola, este es un mensaje de ejemplo para el grupo!"
#     bot.send_message(ID_DEL_GRUPO, mensaje)




if __name__ == "__main__":
    try:
        bot.polling(none_stop=True, timeout=3600)
    except requests.exceptions.ReadTimeout as e:
        print(f"El tiempo espera antes del error es de: {e/60} minutos")



