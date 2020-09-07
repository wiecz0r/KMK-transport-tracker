import json
import requests
from VehiclePosition import VehiclePosition, JSONserializer

class TTSSGetter():
    def __init__(self):
        self.url_t = 'http://www.ttss.krakow.pl/internetservice/geoserviceDispatcher/services/vehicleinfo/vehicles?positionType=CORRECTED'
        self.url_b = 'http://ttss.mpk.krakow.pl/internetservice/geoserviceDispatcher/services/vehicleinfo/vehicles?positionType=CORRECTED'

    def getVehiclePositions(self):
        urls = [self.url_t, self.url_b]
        positions = []

        for url in urls:
            response = requests.get(url).text
            parsed = json.loads(response)['vehicles']
            keys = ["name","latitude","longitude"]
            active_vehicles = [{key: v[key] for key in keys} for v in parsed if not 'isDeleted' in v.keys()]
            for v in active_vehicles:
                name_splitted = v["name"].split(' ')
                v["line"] = name_splitted[0]
                v["name"] = ' '.join(name_splitted[1:])
            pos = [VehiclePosition(v["latitude"] / 3600000.0, v["longitude"] / 3600000.0, \
                None,v["line"],v["name"]) for v in active_vehicles]
            positions.append(pos)
        
        return positions[0], positions[1]
