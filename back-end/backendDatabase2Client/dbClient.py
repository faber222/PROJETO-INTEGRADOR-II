import ctypes
import os
import paho.mqtt.client as mqtt
import pymysql
import time

def publish_to_mqtt(client, idEsp, tabela, ligado):
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
    mqtt_client.connect(MQTT_BROKER, 1883, 60)

    # Criar o tópico com base na tabela e idEsp
    topic = f"{idEsp}{tabela}"

    print(f"valor: {ligado}")
    mqtt_client.publish(topic, str(ligado), qos=1)

    # Desconectar o cliente MQTT
    mqtt_client.disconnect()

def read_and_publish_from_db(client):
    global payload_received  # Declare payload_received as a global variable
    MYSQL_HOST = os.environ.get('MYSQL_HOST', '{IP_MYSQL}')
    MYSQL_USER = os.environ.get('MYSQL_USER', '{USER_MYSQL}')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '{PASSWD_MYSQL}')
    MYSQL_DB = os.environ.get('MYSQL_DB', '{DB_MYSQL}')

    while True:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=3306,
        )

        cursor = connection.cursor()
        # Tabelas a serem lidas e publicadas
        tabelas = ['lampada', 'ar_condicionado']

        for tabela in tabelas:
            select_query = f"SELECT idEsp, ligado FROM {tabela} where id=1"
            cursor.execute(select_query)
            rows = cursor.fetchall()
            for row in rows:
                idEsp, ligado = row
                publish_to_mqtt(client, idEsp, tabela, ligado)

        # Fechar a conexão com o banco de dados
        connection.close()
        # Aguardar 2 segundos antes de realizar a próxima leitura
        time.sleep(2)

# Chamar a função para ler do banco de dados e publicar no MQTT
# Configurar o cliente MQTT
client = mqtt.Client()
MQTT_BROKER = os.environ.get('MQTT_BROKER', '{IP_MQTT}')
MQTT_USERNAME = os.environ.get('MQTT_USERNAME', '{USER_MQTT}')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', '{PASSWD_MQTT}')

while True:
    read_and_publish_from_db(client)