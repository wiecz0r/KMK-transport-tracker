from google.transit import gtfs_realtime_pb2
from ftplib import FTP
from VehiclePosition import VehiclePosition
import paho.mqtt.client as paho
import time

def get_data(ftp):
    data = []
    ftp.retrbinary('RETR VehiclePositions_T.pb',data.append)
    return b''.join(data)

def CreateMQTTclient():
    client = paho.Client()
    client.connect('broker.mqttdashboard.com', 1883)
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
            positions = [VehiclePosition(entity,'Tram') for entity in feed.entity]
            print(positions.toJSON())
            MQTTclient.publish('swswwsws/1235', str(temperature), qos=1)
            time.sleep(5)
    except KeyboardInterrupt:
        print('\nExiting...')
    finally:
        ftp.quit()

if __name__ == "__main__":
    main()
