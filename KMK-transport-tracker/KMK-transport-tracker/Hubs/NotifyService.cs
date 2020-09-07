using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR;

namespace KMK_transport_tracker.Hubs
{
    public class NotifyService
    {
        private readonly IHubContext<MapHub> _hub;
        private string current_T_positions = string.Empty;
        private string current_B_positions = string.Empty;

        public NotifyService(IHubContext<MapHub> hub)
        {
            _hub = hub;
        }

        public Task SendNotificationAsync(string message, string topic)
        {
            var transport_type = topic.Split('/')[1];
            Console.WriteLine("SignalR Sent - " + transport_type);
            switch (transport_type)
            {
                case "trams":
                    current_T_positions = message;
                    break;
                case "buses":
                    current_B_positions = message;
                    break;
                default:
                    return Task.CompletedTask;
            }
            return _hub.Clients.All.SendAsync(transport_type, message);
        }

        public void SendPositionsToClients()
        {
            _hub.Clients.All.SendAsync("trams", current_T_positions);
            _hub.Clients.All.SendAsync("buses", current_B_positions);
        }
    }
}
