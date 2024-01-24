import requests.exceptions
import telebot
from telebot import types
import mysql.connector
from mysql.connector import errorcode
TOKEN = '6746321824:AAGv0cFhzwdwmb5gFtz66LFVyJSJkqe3Gfw'
bot = telebot.TeleBot(TOKEN)


def connectToBD():
    config = {
        'user': 'admin',
        'password': 'Consensus2023*',
        'host': '200.122.249.98',
        'database': 'TelegramBot1',
        'raise_on_warnings': True
    }
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        return connection, cursor
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Usuario o password incorrecto")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)

def validar_existencia_group(groupId):
    try:
        data = []
        connection, cursor = connectToBD()
        sql = 'SELECT * FROM `TelegramBot1`.`grupos` WHERE id_telegram = %s;'
        value = groupId
        cursor.execute(sql,(value,))
        results = cursor.fetchall()
        for row in results:
            data.append([row[0],row[1],row[2],row[3]])
        leng = len(data)
        if leng > 0:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"Ha ocurrido un error {e}")
        return 0

def insert_group(id_group,name_group):
    try:
        connection, cursor = connectToBD()
        sql = 'INSERT INTO `TelegramBot1`.`grupos` (id_telegram, nombre_grupo) VALUES (%s, %s)'
        values = (id_group, name_group)
        cursor.execute(sql,values)
        connection.commit()
        return 1
    except Exception as e:
        print(f"Ha ocurrido un error {e}")
        return 0

@bot.message_handler(commands=['empezar'])
def sendWelcomeMessage(message):
    bot.reply_to(message, 'Bienvenido al Bot STI')

@bot.message_handler(commands=['info'])
def infomationBot(message):
    bot.reply_to(message, 'Este es un bot creado para el envio masivo de mensajes')
    print(message.chat)

@bot.message_handler(commands=['vincular'])
def vinculation(message):
    if message.chat.type == 'supergroup':
        result = validar_existencia_group(str(message.chat.id))
        if result == 1:
            bot.reply_to(message, 'No es posible vincular el bot a este grupo porque ya se encuentra vinculado')
        else:
            insert_group(message.chat.id, message.chat.title)
            bot.reply_to(message, 'Vinculado con exito')
    else:
        bot.reply_to(message, 'Este comando es exclusivo para grupos y no para usuarios.')

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



