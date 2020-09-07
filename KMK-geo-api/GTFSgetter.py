from ftplib import FTP
import zipfile
import io
from VehiclePosition import Trip,JSONserializer,Trips,VehiclePosition
from google.transit import gtfs_realtime_pb2

class GTFSGetter():
    def __init__(self,ftp : FTP):
        self.ftp = ftp
        self.ftp.login()
        self.ftp.cwd('pliki-gtfs')
        self.feed = gtfs_realtime_pb2.FeedMessage()
        self.zip_timestamp_t = ''
        self.zip_timestamp_b = ''
        self.trips_t = []
        self.trips_b = []

    def _getData(self,command):
        data = []
        self.ftp.retrbinary(command,data.append)
        return b''.join(data)

    def getVehiclePositions(self):
        # TRAMS
        timestamp = self.ftp.voidcmd("MDTM GTFS_KRK_T.zip")[4:].strip()
        if timestamp != self.zip_timestamp_t:
            self.zip_timestamp_t = timestamp

            zb = self._getData("RETR GTFS_KRK_T.zip")
            z = zipfile.ZipFile(io.BytesIO(zb))
            routes = {x.split(',')[0:3:2][0] : int(x.split(',')[0:3:2][1].replace('\"','')) \
                for x in z.read('routes.txt').decode('utf-8').split('\r\n')[1:] if len(x) > 1}

            self.trips_t = Trips([Trip([y for i,y in enumerate(x.split(',')[:4]) if i!= 2],routes) \
                for x in z.read("trips.txt").decode('utf-8').split('\r\n')[1:] if len(x)>1])
            

        self.feed.ParseFromString(self._getData("RETR VehiclePositions_T.pb"))
        pos_t = [VehiclePosition(x.vehicle.position.latitude,x.vehicle.position.longitude,\
            self.trips_t.getTrip(x.vehicle.trip.trip_id)) for x in self.feed.entity]

        #BUSES
        timestamp = self.ftp.voidcmd("MDTM GTFS_KRK_A.zip")[4:].strip()
        if timestamp != self.zip_timestamp_b:
            self.zip_timestamp_b = timestamp

            zb = self._getData("RETR GTFS_KRK_A.zip")
            z = zipfile.ZipFile(io.BytesIO(zb))
            routes = {x.split(',')[0:3:2][0] : int(x.split(',')[0:3:2][1].replace('\"','')) \
                for x in z.read('routes.txt').decode('utf-8').split('\r\n')[1:] if len(x) > 1}

            self.trips_b = Trips([Trip([y for i,y in enumerate(x.split(',')[:4]) if i!= 2],routes) \
                for x in z.read("trips.txt").decode('utf-8').split('\r\n')[1:] if len(x)>1])
            

        self.feed.ParseFromString(self._getData("RETR VehiclePositions_A.pb"))
        pos_b = [VehiclePosition(x.vehicle.position.latitude,x.vehicle.position.longitude,\
            self.trips_b.getTrip(x.vehicle.trip.trip_id)) for x in self.feed.entity]
        
        return pos_t, pos_b


