from machine import Pin
from umodbus.serial import Serial as ModbusRTUMaster
from json import dumps
import network
import time
from umqtt.simple import MQTTClient

from secrets import *

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid,psk)
time.sleep(5)

client_id = 'pipico-thermocouple-mbus'
topic_pub = b'sensors/mbus/thermo'

rtu_pins = (Pin(4),Pin(5))
host = ModbusRTUMaster(baudrate=115200, data_bits=8, stop_bits=1, parity=None, pins=rtu_pins, ctrl_pin=15)

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
    
while True:
    res = host.read_holding_registers(slave_addr=2, starting_addr=0, register_qty=22)
    d = {
        "RELAY": res[0],
        "SENSOR": res[1],
        "TIME": res[2],
        "TEMP": res[3] * 0.1,
        "F_C": res[4],
        "OPE": res[5],
        "TEP": res[6] * 0.1,
        "OTP": res[7] * 0.1,
        "BTE": res[8] * 0.1,
        "LTP": res[9] * 0.1,
        "DLY": res[10],
        "OFE": res[11] * 0.1,
        "ALARM": res[12],
        "BEP-SW": res[13],
        "OTP-SW": res[14],
        "LTP-SW": res[15],
        "DLY-SW": res[16],
        "STOP": res[17],
        "ADDR": res[18],
        "BAUDRATE": res[19],
        "SLEEP": res[20],
        "BL": res[21]
    }
    client.publish(topic_pub, dumps(d))
    time.sleep(30)
 