import paho.mqtt.client as mqtt
import pymysql

def on_message(client, userdata, message):
    mensagem = message.payload.decode("utf-8")
    print(f"Mensagem recebida: {mensagem}")


    # Conecte-se ao servidor MySQL
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='PudimAm@ssad0',
        database='Pji',
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

    if message.topic == 'temperature':
        insert_query = "INSERT INTO temperatura (temperatura, idEsp) VALUES (%s, %s)"
    elif message.topic == 'humidity':
        insert_query = "INSERT INTO umidade (umidade, idEsp) VALUES (%s, %s)"
    else:
        print("Tópico incorreto!")
        return

    cursor.execute(insert_query, (valor, chave))
    connection.commit()

    print("Mensagem salva no banco de dados.")


# Configurar o cliente MQTT
client = mqtt.Client()
# Adicionar autenticação com nome de usuário e senha
client.username_pw_set(username='guga', password='espsensors')
client.on_message = on_message

# Conectar ao broker MQTT
client.connect('18.231.159.19', 1883, 60)
client.subscribe('temperature')
client.subscribe('humidity')

# Iniciar o loop para escutar mensagens
client.loop_forever()

