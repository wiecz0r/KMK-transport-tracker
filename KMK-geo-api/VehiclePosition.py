from google.transit import gtfs_realtime_pb2
import json
import enum

class JSONserializer:
    def encode(object):
        return json.dumps(object, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4,ensure_ascii=False)

class VehiclePosition():
    def __init__(self,latitude,longitude,trip=None,line=None, direction=None):
        self.type = "Feature"
        self.geometry = Geometry(latitude,longitude)
        if trip is None:
            self.properties = Properties(line, direction)
        else:
            self.properties = Properties(trip.route, trip.direction)

class Properties():
    def __init__(self,line,direction):
        self.line = line
        self.direction = direction

class Geometry():
    def __init__(self, latitude, longtitude):
        self.type = "Point"
        self.coordinates = [longtitude,latitude]

class Trip():
    def __init__(self, params=None, routes=None):
        self.trip = params[0] if params else 'N/A'
        self.route = routes[params[1]] if params and routes else 'N/A'
        self.direction = params[2] if params else 'N/A'

    def __str__(self):
        return '{} {} {}'.format(self.trip, self.route, self.direction)

class Trips():
    def __init__(self,tripList):
        self.trips = tripList

    def getTrip(self,tripID):
        trip_list = [trip for trip in self.trips if trip.trip == tripID]
        if len(trip_list) == 0:
            return Trip()
        return [trip for trip in self.trips if trip.trip == tripID][0]
