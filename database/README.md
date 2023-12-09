# INSTALAÇÃO BANCO DE DADOS MYSQL
Neste projeto optamos por usar o banco de dados mysqL.

Apesar de ser um banco de dados relacional, ficamos apenas usando o basico.

Na pasta mysql você encontrará o export database do banco de dados que usamos no projeto.

Você pode importar e usar no seu(não recomendado).

Não recomendamos importar devido a ser um banco de dados inseguro e não tão bem implementado, ele foi criado apenas para servir de registro simplório da nossa aplicação. O ideal é que a equipe desenvolva um novo, e use como base o nosso.

Para instalar um banco de dados:
```bash
sudo apt install mysql-server
```
Com isso ja vai instalar tudo que é necessário para rodar o banco de dados.

Por fim, recomenda-se seguir esse tutorial:
[how-to-install-mysql-on-ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04)

## Necessidades do código
No projeto, foi utilizado algumas tabelas, dentre elas:
 - temperatura
 - umidade
 - luminosidade
 - lampada
 - ar_condicionado
  
Demais tabelas são geradas automaticamente pela aplicação web para autenticação do usuário.

Para adaptar, pelo menos as tabelas acima devem ser criadas, e um exemplo de como criar, com as colunas necessárias, estão dentro da pasta mysql.
```SQL
DROP TABLE IF EXISTS `temperatura`;
CREATE TABLE `temperatura` (
  `id` int NOT NULL AUTO_INCREMENT,
  `temperatura` decimal(5,2) DEFAULT NULL,
  `idEsp` int NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4775 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

Nossa estrutura de tabelas do banco de dados Pji era composta da seguinte forma:
```bash
+----------------------------+
| Tables_in_Pji              |
+----------------------------+
| ar_condicionado            |
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
| lampada                    |
| luminosidade               |
| temperatura                |
| umidade                    |
| usuarios                   |
+----------------------------+
```

Nota-se que usamos 4 colunas, e a principal é a coluna temperatura, onde armazenamos o valor da temperatura que a esp coleta.

Para identificar de qual esp veio o dado, usamos outra coluna chamada de idEsp, e nela armazena como se fosse o nome atrelado a essa esp.

Não optamos por UK devido ao fato de precisarmos coletar os dados de temperatura e armazenar a fim de apresentar is dados graficamente na aplicação web.