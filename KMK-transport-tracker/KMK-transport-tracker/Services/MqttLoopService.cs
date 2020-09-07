using System;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using KMK_transport_tracker.Hubs;
using Microsoft.Extensions.Hosting;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Client.Disconnecting;
using MQTTnet.Client.Options;

namespace KMK_transport_tracker.Services
{
    public class MqttLoopService : IHostedService
    {
        private IMqttClient mqttClient;
        private readonly string serverAddress = "mqtt.eclipse.org";
        private NotifyService _notifyService;

        public MqttLoopService(NotifyService notifyService)
        {
            this._notifyService = notifyService;
        }

        public async Task StartAsync(CancellationToken cancellationToken)
        {
            mqttClient = new MqttFactory().CreateMqttClient();
            var options = new MqttClientOptionsBuilder()
                .WithTcpServer(serverAddress)
                .Build();

            mqttClient.UseApplicationMessageReceivedHandler(e =>
            {
                var topic = e.ApplicationMessage.Topic; 
                Console.WriteLine("### RECEIVED APPLICATION MESSAGE ###");
                var msg = Encoding.UTF8.GetString(e.ApplicationMessage.Payload);

                //Console.WriteLine(System.Text.ASCIIEncoding.Unicode.GetByteCount(msg));
                _notifyService.SendNotificationAsync(msg,topic);
            });

            mqttClient.UseConnectedHandler(async e =>
            {
                Console.WriteLine("### CONNECTED TO BROKER ###");

                // Subscribe to a topic
                await mqttClient.SubscribeAsync(new MqttTopicFilterBuilder().WithTopic("kmk_geo_api/trams").Build());
                await mqttClient.SubscribeAsync(new MqttTopicFilterBuilder().WithTopic("kmk_geo_api/buses").Build());

                Console.WriteLine("### SUBSCRIBED ###");
            });

            await mqttClient.ConnectAsync(options);
            if (!mqttClient.IsConnected)
            {
                await mqttClient.ReconnectAsync();
            }
        }

        public async Task StopAsync(CancellationToken cancellationToken)
        {
            if (cancellationToken.IsCancellationRequested)
            {
                var disconnectOption = new MqttClientDisconnectOptions
                {
                    ReasonCode = MqttClientDisconnectReason.NormalDisconnection,
                    ReasonString = "NormalDiconnection"
                };
                await mqttClient.DisconnectAsync(disconnectOption, cancellationToken);
            }
            await mqttClient.DisconnectAsync();
        }
    }
}
