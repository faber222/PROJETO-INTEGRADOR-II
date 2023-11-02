package engtelecom.pji;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class MQTTSubscriber {
    private static final String broker = "tcp://192.168.1.6:1883";
    private static final String topic = "teste";
    private static final String dbUrl = "jdbc:mysql://localhost:3306/teste_local";
    private static final String dbUser = "faber222";
    private static final String dbPassword = "faber180975";

    public void executar() {
        try {
            try (MqttClient client = new MqttClient(broker, MqttClient.generateClientId())) {
                client.setCallback(new MqttCallback() {
                    @Override
                    public void connectionLost(Throwable cause) {}

                    @Override
                    public void messageArrived(String topic, MqttMessage message) {
                        String content = new String(message.getPayload());
                        System.out.println("Mensagem recebida: " + content);
                        saveToDatabase(content);
                    }

                    @Override
                    public void deliveryComplete(IMqttDeliveryToken token) {}
                });
                client.connect();
                client.subscribe(topic);
            }
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    private static void saveToDatabase(String message) {
        try {
            Connection connection = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
            String query = "INSERT INTO tabela (mensagem) VALUES (?)";
            PreparedStatement statement = connection.prepareStatement(query);
            statement.setString(1, message);
            statement.executeUpdate();
            connection.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
