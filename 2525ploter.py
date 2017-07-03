# -*- coding: utf-8 -*-
import serial
import threading
import matplotlib.pyplot as plt
import numpy as np
import time
import copy
import os
from argparse import ArgumentParser

from Twilite2525AReceiver import Twilite2525AReceiver

sensor_data = {}

log = False
log_folder = 'log'
log_path = ''

data_keys = ['rc', 'lq', 'ct', 'ed', 'id', 'ba', 'a1', 'a2', 'x', 'y', 'z', 'ts']

def argv_parser():
    argparser = ArgumentParser()
    argparser.add_argument('--log', action='store_const', const=True, default=False)
    args_param = argparser.parse_args()
    return args_param

def port_reader(file_name='port.txt'):
    with open(file_name, 'r') as p_file:
        port = p_file.readline().strip()
        return port

def received(timestamp, data, length=50):
    # print(timestamp, data['ed'], data['id'], data['ct'], data['lq'], flush=True)
    if log:
        content = str(timestamp)
        for key in data_keys:
            content += ',' + data[key]
        with open(log_path, 'a') as f:
            f.write(content + '\n')

    keys = ['time', 'x', 'y', 'z']
    x = float(data['x'])/100.
    y = float(data['y'])/100.
    z = float(data['z'])/100.
    values = [timestamp, x, y, z]
    ed = data['ed'] + ':' + data['id']
    # print(timestamp, ed, x, y, z)
    if ed in sensor_data.keys():
        if len(sensor_data[ed][keys[0]]) >= length:
            for key, value in zip(keys, values):
                sensor_data[ed][key].pop(0)
        for key, value in zip(keys, values):
            sensor_data[ed][key].append(value)
    else:
        sensor_data[ed] = {}
        for key in keys:
            sensor_data[ed][key] = []
        sensor_data[ed]['time'].append(timestamp)
        sensor_data[ed]['x'].append(x)
        sensor_data[ed]['y'].append(y)
        sensor_data[ed]['z'].append(z)

def plot_data(start_time):
    keys = ['x', 'y', 'z']
    current_node_size = 0
    plot_dict = {}
    while True:
        sensor_data_cp = copy.deepcopy(sensor_data)
        node_size = len(sensor_data_cp.keys())
        if node_size > 0:
            if current_node_size != node_size:
                current_node_size = node_size
                plt.close()
                fig, axs = plt.subplots(node_size, 1)
                plot_dict = {}
                if current_node_size == 1:
                    axs = [axs]
                for ed, ax in zip(sensor_data_cp.keys(), axs):
                    plot_dict[ed] = {}
                    plot_dict[ed]['ax'] = ax
                    time_array = np.array(sensor_data_cp[ed]['time']) - start_time
                    for key in keys:
                        plot_dict[ed][key], = ax.plot(time_array, sensor_data_cp[ed][key])
                    ax.set_ylabel(ed)
            else:
                for ed in plot_dict.keys():
                    time_array = np.array(sensor_data_cp[ed]['time']) - start_time
                    if len(time_array) < 2:
                        continue
                    for key in keys:
                        plot_dict[ed][key].set_data(time_array, sensor_data_cp[ed][key])
                        plot_dict[ed]['ax'].set_xlim((time_array.min(), time_array.max()))
                    plot_dict[ed]['ax'].set_ylim((-3, 3))
                    # print(len(time_array))
        plt.pause(0.05)

def main():
    try:
        # twilite2525
        port = port_reader()
        ser = serial.Serial(port, 115200, timeout=1)

        if log:
            log_file = open(log_path, 'w')
            header = 'timestamp'
            for key in data_keys:
                header += ',' + key
            log_file.write(header + '\n')
            log_file.close()

        twilite = Twilite2525AReceiver(ser, received)
        twilite.run()
        # matplotlib
        start_time = time.time()
        plot_data(start_time)
    except serial.SerialException:
        print('error:could not open port')
        exit(-1)

if __name__ == '__main__':
    args = argv_parser()
    if args.log:
        print('-- logging option')
        log = True
        if not os.path.exists('.' + os.sep + log_folder):
            os.mkdir(log_folder)
        timestamp_str = str(int(time.time()))
        log_path = '.' + os.sep + log_folder + os.sep + timestamp_str + '-log.csv'
    main()