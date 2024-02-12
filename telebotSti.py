import requests.exceptions
import telebot
import datetime
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

def cerrar_conexion(connection, cursor):
    cursor.close()
    connection.close()


def validar_existencia_group(groupId):
    try:
        data = []
        connection, cursor = connectToBD()
        sql = 'SELECT * FROM `TelegramBot1`.`grupos` WHERE id_telegram = %s;'
        value = groupId
        cursor.execute(sql, (value,))
        results = cursor.fetchall()
        for row in results:
            data.append([row[0], row[1], row[2], row[3]])
        leng = len(data)
        if leng > 0:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"Ha ocurrido un error {e}")
        return 0
    finally:
        cerrar_conexion(connection, cursor)


def insert_group(id_group, name_group):
    try:
        connection, cursor = connectToBD()
        sql = 'INSERT INTO `TelegramBot1`.`grupos` (id_telegram, nombre_grupo) VALUES (%s, %s)'
        values = (id_group, name_group)
        cursor.execute(sql, values)
        connection.commit()
        return 1
    except Exception as e:
        print(f"Ha ocurrido un error {e}")
        return 0
    finally:
        cerrar_conexion(connection, cursor)

def insert_group_logs(usuario, id_grupo_telegram):
    try:
        connection, cursor = connectToBD()
        dateTime =datetime.datetime.now()
        accion = "Asociacion de grupo de telegram"
        sql = 'INSERT INTO `TelegramBot1`.`grupos_logs` (usuario, dateTime, accion, id_grupo_telegram) VALUES (%s, %s,%s,%s)'
        values = (usuario, dateTime, accion, id_grupo_telegram)
        cursor.execute(sql, values)
        connection.commit()
        return  1
    except Exception as e:
        print(f"Ha ocurrido un error {e}")
        return 0
    finally:
        cerrar_conexion(connection, cursor)

# @bot.message_handler(commands=['empezar'])
# def sendWelcomeMessage(message):
#     bot.reply_to(message, 'Bienvenido al Bot STI')
#
# @bot.message_handler(commands=['info'])
# def infomationBot(message):
#     bot.reply_to(message, 'Este es un bot creado para el envio masivo de mensajes')
#     print(message.chat)

@bot.message_handler(commands=['vincular_sti'])
def vinculation(message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group':
        result = validar_existencia_group(str(message.chat.id))
        if result == 1:
            bot.reply_to(message, 'No es posible vincular el bot a este grupo porque ya se encuentra vinculado')
        else:
            insert = insert_group(message.chat.id, message.chat.title)
            if insert == 1:
                username = message.from_user.first_name + " " + message.from_user.last_name
                insert_group_logs(username, message.chat.id)
                bot.reply_to(message, 'Vinculado con exito')

    else:
        bot.reply_to(message, 'Este comando es exclusivo para grupos y no para usuarios.')

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True, timeout=3600)
    except requests.exceptions.ReadTimeout as e:
        print(f"El tiempo espera antes del error es de: {e/60} minutos")



