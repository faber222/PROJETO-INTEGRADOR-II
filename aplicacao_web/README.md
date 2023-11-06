# Backend da aplicação web
## Estado Atual 🚀

Autenticação feita inserindo os dados do usuário de forma segura no mysql.

Abaixo passo a passo recomendado caso queira deixar as dependências do projeto em um venv (opcional porém recomendado)
### Criar o Ambiente Virtual

```shell
python3 -m venv venv
```

### Pra ativar o Ambiente Virtual

No windows:

```shell
venv\Scripts\activate
```

No linux:

```shell
source venv/bin/activate
```

### Dependências de sistema
```shell
xargs -a requirements-system.txt sudo apt-get install
```

### Instalação de dependências

```shell
pip install -r requirements.txt
```

### Configurando DB
precisa ter o servidor mysql instalado na tua maquina local e colocar as credenciais de autenticação em project/settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Pji1234',
        'USER': 'root',
        'PASSWORD': 'Brc1234@',
        'PORT': 3306,
        'HOST': '127.0.0.1'
    }
}
```
deve substituir NAME pelo nome da tua conexão, o USER geralmente o padrão é root, o password que tu colocar pro teu mysqlserver quando tu instala ele, e o host local que vai ser 127.0.0.1 (pra desenvolvimento). Tem bastante informação no google pra configurar o mysqlserver no teu pc caso nunca tenha feito, chatgpt também pode fazer passo-a-passo ensinando.


### Executando a aplicação web
Precisa estar no diretório aplicacao_web e executar o seguinte comando:
```python
python3 manage.py runserver
```
