# -*- coding:utf-8 -*-

import os
import time
import threading

# data_keys = ['rc', 'lq', 'ct', 'ed', 'id', 'ba', 'a1', 'a2', 'x', 'y', 'z']

class Twilite2525AReceiver():
    def __init__(self, ser, callback):
        super(Twilite2525AReceiver, self).__init__()
        self.ser = ser
        self.callback = callback
        self.stop_event = threading.Event()

    def _reading(self):
        while not self.stop_event.is_set():
            line = self.ser.readline()
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
                    self.callback(timestamp, data_dict)
                except IndexError:
                    print('IndexError')
                    pass
                except ValueError:
                    print('ValueError')
                    pass
    
    def run(self):
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._reading)
        self.thread.setDaemon(True)
        self.thread.start()
        
    def stop(self):
        self.stop_event.set()
        self.thread.join()
    
    def close(self):
        self.ser.close()