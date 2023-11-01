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
