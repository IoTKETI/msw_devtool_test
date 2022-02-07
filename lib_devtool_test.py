#!/usr/bin/python3
import json
import random
import sys
import threading
import os
import time
import paho.mqtt.client as mqtt

i_pid = os.getpid()
argv = sys.argv

control_topic = ''
data_topic = ''

testQ = {}

broker_ip = 'localhost'
port = 1883

control_msg = ''


def testQ_init():
    testQ['test1'] = 0.0
    testQ['test2'] = 0.0
    testQ['test3'] = 0.0
    testQ['test4'] = 0.0
    testQ['test5'] = 0.0
    testQ['test6'] = 0.0
    testQ['test7'] = 0.0
    testQ['test8'] = 0.0
    testQ['test9'] = 0.0
    testQ['test10'] = 0.0


def on_connect(client, userdata, flags, rc):
    global control_topic
    global broker_ip

    print('[msw_mqtt_connect] connect to ', broker_ip)
    lib_mqtt_client.subscribe(control_topic, 0)
    print('[lib]control_topic\n', control_topic)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    global data_topic
    global control_topic
    global control_msg

    message = str(msg.payload.decode("utf-8"))
    if message == 'OFF':
        print('receive OFF')
        control_msg = False

    elif message == 'ON':
        print('receive ON')
        control_msg = True


def msw_mqtt_connect():
    global lib_topic
    global lib_mqtt_client
    global broker_ip
    global port

    lib_topic = ''

    lib_mqtt_client = mqtt.Client()
    lib_mqtt_client.on_connect = on_connect
    lib_mqtt_client.on_disconnect = on_disconnect
    lib_mqtt_client.on_subscribe = on_subscribe
    lib_mqtt_client.on_message = on_message
    lib_mqtt_client.connect(broker_ip, port)
    lib_mqtt_client.loop_start()

    return lib_mqtt_client


def missionPortOpening():
    global testQ
    global lib_mqtt_client
    global data_topic
    global control_msg

    while True:
        testQ['test1'] = round(random.random(), 2)
        testQ['test2'] = round(random.random(), 2)
        testQ['test3'] = round(random.random(), 2)
        testQ['test4'] = round(random.random(), 2)
        testQ['test5'] = round(random.random(), 2)
        testQ['test6'] = round(random.random(), 2)
        testQ['test7'] = round(random.random(), 2)
        testQ['test8'] = round(random.random(), 2)
        testQ['test9'] = round(random.random(), 2)
        testQ['test10'] = round(random.random(), 2)

        if control_msg:
            lib_mqtt_client.publish(data_topic, json.dumps(testQ))
        time.sleep(1)


def main():
    global lib_mqtt_client
    global control_topic
    global data_topic
    global broker_ip
    global port
    global lib
    global control_msg

    my_lib_name = 'lib_devtool_test'
    my_msw_name = 'msw'+ my_lib_name[3:] + '_' + 'msw'+ my_lib_name[3:]

    try:
        lib = dict()
        with open('./' + my_msw_name + '/' + my_lib_name + '.json', 'r') as f:
            lib = json.load(f)
            lib = json.loads(lib)

    except Exception as e:
        lib = dict()
        lib["name"] = my_lib_name
        lib["target"] = 'armv6'
        lib["description"] = "[name] [portnum] [baudrate]"
        lib["scripts"] = './' + my_lib_name + ' /dev/ttyUSB4 115200'
        lib["data"] = ['Test']
        lib["control"] = ['Control_Test']
        lib = json.dumps(lib, indent=4)
        lib = json.loads(lib)

        # with open('./' + my_msw_name + '/' + my_lib_name + '.json', 'w', encoding='utf-8') as json_file:
        with open('./' + my_lib_name + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(lib, json_file, indent=4)

    lib['serialPortNum'] = argv[1]
    lib['serialBaudrate'] = argv[2]

    control_topic = '/MUV/control/' + lib["name"] + '/' + lib["control"][0]
    data_topic = '/MUV/data/' + lib["name"] + '/' + lib["data"][0]

    msw_mqtt_connect()

    control_msg = True
    t = threading.Thread(target=missionPortOpening, )
    t.start()


if __name__ == '__main__':
    main()
