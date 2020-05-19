from google.transit import gtfs_realtime_pb2
import json
import enum

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class VehiclePosition(Object):
    def __init__(self,feedEntity : gtfs_realtime_pb2.FeedEntity,vehicle_type):
        self.vehicle_type = vehicle_type
        self.line = ""
        self.vehicle_id = feedEntity.id
        self.position = Position(feedEntity.vehicle.position.latitude,feedEntity.vehicle.position.longitude)
        self.timestamp = feedEntity.vehicle.timestamp

    def __str__(self):
        return self.toJSON()

class Position():
    def __init__(self,latitude,longitude):
        self.latitude = latitude
        self.longitude = longitude