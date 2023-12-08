import os
import paho.mqtt.client as mqtt
import pymysql

def on_message(client, userdata, message):
    mensagem = message.payload.decode("utf-8")
    print(f"Mensagem recebida: {mensagem}")

    MYSQL_HOST = os.environ.get('MYSQL_HOST', '{IP_MYSQL}')
    MYSQL_USER = os.environ.get('MYSQL_USER', '{USER_MYSQL}')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '{PASS_MYSQL}')
    MYSQL_DB = os.environ.get('MYSQL_DB', '{DB_NAME}')

    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=3306,
    )

    pares = mensagem.split(';')

    if len(pares) >= 2:
        chave = pares[0]
        valor = pares[1]
        print(f"Chave: {chave}, Valor: {valor}")
    else:
        print("A mensagem não contém um par chave-valor válido.")

    cursor = connection.cursor()

    # Usamos 3 tabelas, temperatura, umidade e luminosidade
    if message.topic == 'temperature':
        insert_query = "INSERT INTO temperatura (temperatura, idEsp) VALUES (%s, %s)"
    elif message.topic == 'humidity':
        insert_query = "INSERT INTO umidade (umidade, idEsp) VALUES (%s, %s)"
    elif message.topic == 'lumens':
        insert_query = "INSERT INTO luminosidade (ligado, idEsp) VALUES (%s, %s)"
    else:
        print("Tópico incorreto!")
        return
    # A String chave é o idEsp, que referencia a qual esp o user possui
    cursor.execute(insert_query, (valor, chave))
    connection.commit()

    print("Mensagem salva no banco de dados.")

# Configurar o cliente MQTT
client = mqtt.Client()

MQTT_USERNAME = os.environ.get('MQTT_USERNAME', '{USER_MQTT}')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', '{PASS_MQTT}')
MQTT_BROKER = os.environ.get('MQTT_BROKER', '{IP_BROCKER}')

# Adicionar autenticação com nome de usuário e senha
client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
client.on_message = on_message

# Conectar ao broker MQTT
client.connect(MQTT_BROKER, 1883, 60)

# Criamos 3 tópicos mqtt
client.subscribe('temperature')
client.subscribe('humidity')
client.subscribe('lumens')

# Iniciar o loop para escutar mensagens
client.loop_forever()