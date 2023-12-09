# Nome da imagem que servirá de base
FROM ubuntu:latest
WORKDIR /app

RUN apt update -y && apt upgrade -y 
RUN apt install mosquitto mosquitto-clients -y
RUN apt install nano -y
RUN net-tools -y
