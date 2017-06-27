# -*- coding: utf-8 -*-
import serial
import threading
import matplotlib.pyplot as plt
import time
import os

from Twilite2525AReceiver import Twilite2525AReceiver

port = 'COM5'
log_folder = 'log'

sensor_data = {}
data_keys = ['rc', 'lq', 'ct', 'ed', 'id', 'ba', 'a1', 'a2', 'x', 'y', 'z']

def received(timestamp, data, log_path):
    print(timestamp, data['ed'], data['id'], data['ct'], data['lq'], flush=True)
    content = str(timestamp)
    for key in data_keys:
        content += ',' + data[key]
    with open(log_path, 'a') as f:
        f.write(content + '\n')

def main():
    if not os.path.exists('.' + os.sep + log_folder):
        os.mkdir(log_folder)
    timestamp_str = str(int(time.time()))
    log_path = '.' + os.sep + log_folder + os.sep + timestamp_str + '-log.csv'
    log_file = open(log_path, 'w')
    header = 'timestamp'
    for key in data_keys:
        header += ',' + key
    log_file.write(header + '\n')
    log_file.close()

    # twilite2525
    ser = serial.Serial(port, 115200, timeout=1)

    while True:
        line = ser.readline()
        field = line.decode('utf-8').strip()
        sline = field.split(':')
        length = len(sline)
        if length == 13:
            timestamp = time.time()
            data_dict = {}
            try:
                for data in sline:
                    if '=' in data:
                        key = data.split('=')[0]
                        val = data.split('=')[1]
                        data_dict[key] = val
                received(timestamp, data_dict, log_path)
            except IndexError:
                print('IndexError')
                pass
            except ValueError:
                print('ValueError')
                pass
if __name__ == '__main__':
    main()