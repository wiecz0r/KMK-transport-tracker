"use strict";
var mymap = L.map('mapid').setView([50.061849, 19.936677], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(mymap);

var tramLayer = L.geoJSON();
tramLayer.addTo(mymap);

var busLayer = L.geoJSON();
busLayer.addTo(mymap);

var connection = new signalR.HubConnectionBuilder().withUrl("/geo").build();

connection.on("trams", function (message) {
    console.log("Received trams positions")
    var msg = JSON.parse(message);
    mymap.removeLayer(tramLayer);
    tramLayer = L.geoJSON(msg,
        {
            pointToLayer: function (feature, latlng) {
                var myIcon = L.divIcon({
                    html: feature.properties.line,
                    className: 'my-div-icon-tram',
                    iconSize: [30, 30]
                });
                return L.marker(latlng, { icon: myIcon });
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup("<b>" + feature.properties.line + "</b><br>" + feature.properties.direction);
            }
        }
    );
    tramLayer.addTo(mymap);
});

connection.on("buses", function (message) {
    console.log("Received buses positions")
    var msg = JSON.parse(message);
    mymap.removeLayer(busLayer);
    busLayer = L.geoJSON(msg,
        {
            pointToLayer: function (feature, latlng) {
                var myIcon = L.divIcon({
                    html: feature.properties.line,
                    className: 'my-div-icon-bus',
                    iconSize: [30, 30]
                });
                return L.marker(latlng, { icon: myIcon });
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup("<b>" + feature.properties.line + "</b><br>" + feature.properties.direction);
            }
        }
    );
    busLayer.addTo(mymap);
});

connection.start().then(() => connection.invoke("GetCurrentPositions").catch(err => console.error(err)));



