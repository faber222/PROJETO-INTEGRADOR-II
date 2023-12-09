# INSTALAÇÃO BROCKER-MQTT
Para fazer tudo funcionar, é necessário que o servidor principal esteja rodando, e optamos por usar o brocker-mqtt para isso.

Ele servirá como ponte entre a ESP e o banco de dados.

O BROCKER-MQTT funciona da seguinte forma, ele faz o intermédio de fila de mensagens, onde dois assinantes de um tópico, podem publicar e subscrever.
Ou seja, um envia dados e o outro lê esses dados do tópico participante.

Por exemplo:
 - João resolve se inscrever no tópico projeto
 - Carlos conhece o tópico projeto e resolve publicar mensagens nele
 - Carlos envia mensagens no tópico sem saber que pode ter algum inscrito ou não
 - João como ja se inscreveu, começa a receber mensagens vinda no tópico, e o mesmo não sabe quem mandou

Para instalar o BROCKER-MQTT, usaremos docker para isso e primeiro devemos instalar o docker na máquina:
```bash
./installDocker.sh
```
Com o docker ja instalado, basta executar:
```bash
docker compose up --build -d &
```

Com isso, seu servidor brocker ja vai estar online e podendo hospedar a fila de mensagens.

Lembre-se de alterar o arquivo password.txt para adicionar as suas credenciais de acesso, dê uma pesquisada de como alterar e colocar cryptografia.

Porém, deve ser alterado dentro do docker e não fora, pois apenas a aplicação mosquitto vai criptografar as senhas no padrão necessário.