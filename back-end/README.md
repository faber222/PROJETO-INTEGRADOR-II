# INSTRUÇÕES DE USO

## Instalação docker compose
Necessário instalar o docker compose na máquina.

Basta executar o programa:
```bash
./installDocker.sh
```

Com o docker compose instalado, agora é hora de editar o arquivo conforme os dados solicitados: dentro de cada código.

Lembre-se, para executar essa aplicação, você ja ter rodando o docker compose do MQTT e ter o mysql instalado na sua máquina, com usuario e senha definidos conforme necessário.

## Subindo aplicação de coleta de dados
Para subir a aplicação, na raiz desta pasta, basta executar:
```bash
docker compose up --build -d &
```

Se tudo ocorreu bem, você ja terá sua aplicação coletando dados do MQTT e publicando no seu banco de dados.

### Para verificar se o docker está ativo:
```bash
docker compose ps
```

### Para verificar se criou a imagem:
```bash
docker images
```

### Para encerrar o serviço
```bash
docker compose down 
```