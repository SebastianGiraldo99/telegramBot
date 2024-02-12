import  datetime
import mysql.connector
import telebot
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

def get_date_hour_act():
    days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    allDate = datetime.datetime.now()
    day = allDate.isoweekday()
    hour = allDate.hour
    return  days[day-1],hour


def find_messages():
    try:
        data = []
        string_day, hour = get_date_hour_act()
        connection, cursor = connectToBD()
        sql = f'''
                   SELECT G.id_telegram, M.mensaje
                   FROM `TelegramBot1`.`grupo_mensajes` AS GM
                   INNER JOIN `TelegramBot1`.`grupos` AS G ON GM.id_grupo = G.id
                   INNER JOIN `TelegramBot1`.`mensajes` AS M ON GM.id_mensaje = M.id
                   WHERE GM.{string_day} = 1 AND GM.hora_envio = %s AND M.estado = 1;
               '''
        parameters = (hour,)
        cursor.execute(sql, parameters)
        results = cursor.fetchall()
        for result in results:
            data.append(result)
        for id_telegram, message in data:
            send_messages(id_telegram, message)
        return 1
    except Exception as e:
        return f"El error es: {e}"
    finally:
        cerrar_conexion(connection, cursor)


def send_messages(id_telegram, message):
    print(f"Id telegram {id_telegram} and message {message}")
    bot.send_message(id_telegram, message)


if __name__ == '__main__':
    try:
        print("Empieza la ejecucion")
        messages = find_messages()
        days, hour = get_date_hour_act()
    except Exception as e:
        print(f"Error al ejecutar el programa {e}")