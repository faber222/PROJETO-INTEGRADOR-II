package engtelecom.pji;

import java.io.IOException;
import java.net.SocketException;
import java.net.UnknownHostException;

public class App {

    public static void main(String[] args) throws SocketException, UnknownHostException, IOException {
        MQTTSubscriber mqttSubscriber = new MQTTSubscriber();
        mqttSubscriber.executar();
    }
}