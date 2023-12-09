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
    private static final String broker = "tcp://{MYSQL_IP}:1883";
    private static final String topic = "{MQTT_TOPIC}";
    private static final String dbUrl = "jdbc:mysql://localhost:3306/teste_local";
    private static final String dbUser = "{MYSQL_USER}";
    private static final String dbPassword = "{MYSQL_PWD}";

    public void executar() {
        try {
            try (MqttClient client = new MqttClient(broker, MqttClient.generateClientId())) {
                client.setCallback(new MqttCallback() {
                    @Override
                    public void connectionLost(Throwable cause) {
                    }

                    @Override
                    public void messageArrived(String topic, MqttMessage message) throws ClassNotFoundException {
                        String content = new String(message.getPayload());
                        System.out.println("Mensagem recebida: " + content);
                        saveToDatabase(content);
                    }
                    
                    @Override
                    public void deliveryComplete(IMqttDeliveryToken token) {
                    }
                });
                client.connect();
                client.subscribe(topic);
            }
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    private static void saveToDatabase(String message) {
        Connection connection = null;
        PreparedStatement statement = null;
        try {
            Class.forName("com.mysql.cj.jdbc.Driver"); // Registrar o driver JDBC

            connection = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
            String query = "INSERT INTO tabela (mensagem) VALUES (?)";
            statement = connection.prepareStatement(query);

            statement.setString(1, message);
            statement.executeUpdate();
        } catch (SQLException | ClassNotFoundException e) {
            e.printStackTrace();
        } finally {
            try {
                if (statement != null) {
                    statement.close();
                }
                if (connection != null) {
                    connection.close();
                }
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}
