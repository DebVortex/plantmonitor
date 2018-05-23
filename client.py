# encoding: utf-8
import json

import click
from miplant import MiPlant
from paho.mqtt.client import Client

from version import VERSION


@click.command()
@click.option('--broker', help='MQTT Broker to send data to.')
@click.option('--port', default=1883, help='Port of the MQTT Server.')
@click.option('--interface', default=0, help='Interface number of the bluetooth device.')
@click.version_option(version=VERSION)
def main(broker, port, interface):
    """Scan for all MiPlant devicesself.

    Send via MQTT if broker is provided. Print to console otherwise.
    """
    sensors = discover_and_scan(interface)
    if broker:
        client = Client()
        client.connect(broker, port)
        client.loop_start()
        for sensor in sensors:
            payload = json.dumps({
                'battery': sensor.battery,
                'temperature': sensor.temperature,
                'light': sensor.light,
                'moisture': sensor.moisture,
                'conductivity': sensor.conductivity
            })
            channel = "sensors/plantsensors/{addr}".format(addr=sensor.address)
            client.publish(channel, json.dumps(payload))
        client.loop_stop()
    else:
        for sensor in sensors:
            print('--------------------------')
            print('Address: {addr}'.format(addr=sensor.address))
            print('Battery level: {bat}'.format(bat=sensor.battery))
            print('Temperature: {temp} °C'.format(temp=sensor.temperature))
            print('Light: {light} lx'.format(light=sensor.light))
            print('Moisture: {moist}'.format(moist=sensor.moisture))
            print('Conductivity: {cond} µS/cm'.format(cond=sensor.conductivity))


def discover_and_scan(interface):
    sensors = MiPlant.discover(interface_index=0, timeout=5)
    [sensor.read() for sensor in sensors]
    return sensors


if __name__ == '__main__':
    main()
