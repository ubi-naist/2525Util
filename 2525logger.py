# -*- coding: utf-8 -*-
import serial
import threading
import time
import os

from Twilite2525AReceiver import Twilite2525AReceiver

log_folder = 'log'
sensor_data = {}
data_keys = ['rc', 'lq', 'ct', 'ed', 'id', 'ba', 'a1', 'a2', 'x', 'y', 'z', 'ts']

def port_reader(file_name='port.txt'):
    with open(file_name, 'r') as p_file:
        port = p_file.readline().strip()
        return port

def received(timestamp, data):
    try:
        print(timestamp, data['ed'], data['id'], data['ct'], data['lq'], flush=True)
        content = str(timestamp)
        for key in data_keys:
            content += ',' + data[key]
        with open(log_path, 'a') as f:
            f.write(content + '\n')
    except KeyError:
        print('KeyError')
        print(data)
    
def main():
    log_file = open(log_path, 'w')
    header = 'timestamp'
    for key in data_keys:
        header += ',' + key
    log_file.write(header + '\n')
    log_file.close()

    print('---start---')
    # twilite2525
    try:
        port = port_reader()
        ser = serial.Serial(port, 115200, timeout=1)
        twilite = Twilite2525AReceiver(ser, received)
        twilite.run()
        input()
        twilite.stop()
        twilite.close()
        print('--- finish ---')

    except serial.SerialException:
        print('error:could not open port')
        exit(-1)

if __name__ == '__main__':
    if not os.path.exists('.' + os.sep + log_folder):
        os.mkdir(log_folder)
    timestamp_str = str(int(time.time()))
    log_path = '.' + os.sep + log_folder + os.sep + timestamp_str + '-log.csv'
    main()
