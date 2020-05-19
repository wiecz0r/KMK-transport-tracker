from google.transit import gtfs_realtime_pb2
from ftplib import FTP
from VehiclePosition import VehiclePosition, JSONserializer
import paho.mqtt.client as paho
import time, sys

def get_data(ftp):
    data = []
    ftp.retrbinary('RETR VehiclePositions_A.pb',data.append)
    return b''.join(data)

def CreateMQTTclient():
    client = paho.Client()
    client.connect('mqtt.eclipse.org', 1883)
    client.loop_start()
    return client

def main():
    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        ftp = FTP('ztp.krakow.pl')

        ftp.login()
        ftp.cwd('pliki-gtfs')

        MQTTclient = CreateMQTTclient()

        while(True):
            feed.ParseFromString(get_data(ftp))
            positions = JSONserializer.encode([VehiclePosition(entity,'T') for entity in feed.entity])
            # positions = "ala ma kota"
            print(sys.getsizeof(positions))
            MQTTclient.publish('kmk_geo_api/positions', positions, qos=1)
            time.sleep(5)
    except KeyboardInterrupt:
        print('\nExiting...')
    finally:
        ftp.quit()

if __name__ == "__main__":
    main()
