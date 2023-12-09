# PROJETO ESP-32
Para este projeto, usamos a ESP32 para coleta de dados de temperatura, umidade e luminosidade do ambiente, e todos os dados são enviados via mqtt para a nuvem.

Os dados são coletados usando LDR, ADS, DHT, todos componentes que fixamos na esp para poder funcionar.

A lógica do código é simples, pois só tem coleta, envio e recebimento de comandos, porém é possivel alterar para permitir a esp receber comandos de forma mais facil.

A ESP32 possui dois núcleos, e podemos usufruir de cada núcleo, onde é possivel alterar o código para deixar um núcleo da esp ouvindo no tópico e aguardando comandos, e outro núcleo escrevendo no tópico com os dados coletados.