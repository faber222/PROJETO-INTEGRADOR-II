import pymysql
from random import uniform
from time import sleep

# Conecte-se ao servidor MySQL
connection = pymysql.connect(
    host ='127.0.0.1',
    user ='root',
    password ='Brc1234@',
    database ='Pji1234',
    port =  3306,
)

cursor = connection.cursor()

while True:
    temperatura = round(uniform(20.0, 30.0), 2)
    umidade = round(uniform(40.0, 60.0), 2)

    # Insira os dados na tabela
    query = "INSERT INTO dados_temperatura_umidade (temperatura, umidade) VALUES (%s, %s)"
    data = (temperatura, umidade)
    cursor.execute(query, data)

    connection.commit()

    print(f"Dados inseridos - Temperatura: {temperatura}°C, Umidade: {umidade}%")

    sleep(10)  # Aguarde 10 segundos antes de inserir os próximos dados

cursor.close()
connection.close()