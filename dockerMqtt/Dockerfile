# Nome da imagem que servirá de base
FROM ubuntu:latest
WORKDIR /app

RUN apt update -y && apt upgrade -y 
RUN apt install mosquitto mosquitto-clients -y
RUN apt install nano -y
RUN net-tools -y

# RUN sudo mosquitto_passwd -c /etc/mosquitto/passwd root admin admin
# password_file /etc/mosquitto/passwd

# nano /etc/mosquitto/conf.d/default.conf
# allow_anonymous false
# service mosquitto restart