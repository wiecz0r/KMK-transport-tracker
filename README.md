# KMK-transport-tracker
Consists of two subprojects:
* KMK-geo-api - Python service to parse KMK vehicle positions from external API and send to MQTT Broker
* KMK-transport-tracker - ASP.NET Core Web App to see vehicle positions - DEMO: https://kmk-transport-tracker.herokuapp.com/

To install pip packages needed for KMK-geo-api:
```bash
python3 -m pip install -r requirements.txt
```
Run:
```bash
python3 transport.py [ttss|gtfs]
```
* gtfs: use vehicle positions from gtfs data from ftp://ztp.krakow.pl/
* ttss: use vehicle positions from json data from http://www.ttss.krakow.pl/internetservice/geoserviceDispatcher/services/vehicleinfo/vehicles?positionType=CORRECTED and http://ttss.mpk.krakow.pl/internetservice/geoserviceDispatcher/services/vehicleinfo/vehicles?positionType=CORRECTED
