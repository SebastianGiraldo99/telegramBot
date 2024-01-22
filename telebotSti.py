import telebot
from telebot import types

TOKEN = 'TOKEN_HERE'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['empezar'])
def sendWelcomeMessage(message):
    bot.reply_to(message, 'Bienvenido al Bot STI')

@bot.message_handler(commands=['info'])
def infomationBot(message):
    bot.reply_to(message, 'Este es un bot creado para el envio masivo de mensajes')

##Enviar mensajes a un grupo en especifico usando el nombre del grupo como identificador.
@bot.message_handler(commands=['buenosDias'])
def buenosDiasGrupo(message):
    if message.chat.title == 'PruebaBot':
        bot.reply_to(message, f"Este es un mensaje personalizado para el grupo {message.chat.title}")
    else:
        bot.reply_to(message, 'No es posible dar informacion en este grupo')
    print(message.chat)


if __name__ == "__main__":
    bot.polling(none_stop=True)



