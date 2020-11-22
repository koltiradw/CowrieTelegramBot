import psutil
import time
import datetime
import os
import json
import subprocess

PATH = "time_slices/time_slice.json"

def get_pid():
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if proc.info['name'] == 'twistd':
            return proc.info['pid']

class TimeSlice():
    def __init__(self):
        self._out = open(PATH, "w")
        self._pid = get_pid()
    
    def collect_time_slices(self):
        if datetime.datetime.now().hour == 0:
            self._out.close()
            os.remove(PATH)
            self._out = open(PATH, "w")
        else:
            json_slice = self._create_time_slice()
            json.dump(json_slice, self._out)
            self._out.write("\n")
            self._out.flush()

    def _create_time_slice(self):
        mem_usage        = 0
        cpu_usage        = 0
        cowrie_mem_usage = 0
        cowrie_cpu_usage = 0
        current_time     = datetime.datetime.now().strftime('%H:%M:%S')
        for i in range(30):
            mem_usage        += psutil.virtual_memory()[2]
            cpu_usage        += psutil.cpu_percent(interval = 1)
            cowrie_mem_usage += psutil.Process(self._pid).memory_percent()
            cowrie_cpu_usage += psutil.Process(self._pid).cpu_percent(interval = 1)

        return {"mem_usage"        : mem_usage / 30,
                "cpu_usage"        : cpu_usage / 30,
                "cowrie_mem_usage" : cowrie_mem_usage / 30,
                "cowrie_cpu_usage" : cowrie_cpu_usage / 30,
                "current_time"     : current_time
               }





