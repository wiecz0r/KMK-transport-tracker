using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR;

namespace KMK_transport_tracker.Hubs
{
    public class MapHub : Hub
    {
        private NotifyService _notify_service;

        public MapHub(NotifyService notifyService)
        {
            _notify_service = notifyService;
        }

        public async Task Send(string message)
        {
            await Clients.All.SendAsync("Msg", message);
        }

        public void GetCurrentPositions()
        {
            _notify_service.SendPositionsToClients();
        }
    }
}
