from google.transit import gtfs_realtime_pb2
from ftplib import FTP
from VehiclePosition import VehiclePosition, JSONserializer
import paho.mqtt.client as paho
import time, sys
from GTFSgetter import GTFSGetter
from TTSSgetter import TTSSGetter
import traceback

def CreateMQTTclient():
    client = paho.Client()
    client.connect('mqtt.eclipse.org', 1883)
    client.loop_start()
    return client

def main():
    try:
        MQTTclient = CreateMQTTclient()
        trams = ''
        buses = ''
        cmd = ''

        if len(sys.argv) != 2:
            print("Wrong command - pass 'ttss' or 'gtfs'")
            return

        cmd = sys.argv[1]

        if cmd == 'gtfs':
            ftp = FTP('ztp.krakow.pl')
            dataGetter = GTFSGetter(ftp)
        elif cmd == 'ttss':
            dataGetter = TTSSGetter()
        else:
            print("Wrong command - pass 'ttss' or 'gtfs'")
            return

        while(True):
            try:
                trams_pos, bus_pos = dataGetter.getVehiclePositions()
                new_trams = JSONserializer.encode(trams_pos)
                new_buses = JSONserializer.encode(bus_pos)
                print(len(trams_pos),len(bus_pos))
                if trams != new_trams:
                    trams = new_trams
                    MQTTclient.publish('kmk_geo_api/trams', trams, qos=1, retain=True)
                    print("trams positions published")
                if buses != new_buses:
                    buses = new_buses
                    MQTTclient.publish('kmk_geo_api/buses', buses, qos=1, retain=True)
                    print("buses positions published")
            except Exception as e:
                traceback.print_exc()
            finally:
                time.sleep(5)
    except KeyboardInterrupt:
        print('\nExiting...')
    finally:
        if cmd == 'gtfs':
            ftp.quit()

if __name__ == "__main__":
    main()
