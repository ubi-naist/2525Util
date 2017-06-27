# -*- coding:utf-8 -*-

import threading
import time

class Twilite2525AReceiver(threading.Thread):
    def __init__(self, ser, callback):
        super(Twilite2525AReceiver, self).__init__()
        self.ser = ser
        self.callback = callback

    def run(self):
        while True:
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
                    if self.callback is not None:
                        self.callback(timestamp, data_dict)
                except IndexError:
                    if self.callback is not None:
                        self.callback(timestamp, None)
                except ValueError:
                    if self.callback is not None:
                        self.callback(timestamp, None)
