import os
import psutil
import datetime

def get_common_system_state():
    mem_usage   = psutil.virtual_memory()
    disk_usage  = psutil.disk_usage('/')
    cpu_usage   = psutil.cpu_percent(interval = 1.0)
    system_info = ""

    system_info += "Memory usage: "                    + str(mem_usage[2])  + "%"       + "\n"
    system_info += "CPU usage: "                       + str(cpu_usage)     + "%"       + "\n" 
    system_info += "Disk usage: "                      + str(disk_usage[3]) + "%"       + "\n"
    system_info += "Boot time: "                       + datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    return system_info
