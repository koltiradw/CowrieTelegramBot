import json
from splitstream import splitfile
import datetime


def get_minutes_from_str(str_time):
    return int(str_time[3:][:2])

def get_hour_from_str(str_time):
    return int(str_time[:2])

class Collector():
    @classmethod
    def __init__(self, path):
        self.path = path
    
    @classmethod
    def collect(self):
        slices = self._read_log()
        return self._get_stats(slices)

    @classmethod
    def _read_log(self):
        list_of_dict_resp = []
        with open(self.path, "r") as slices_file:
            for json_str in splitfile(slices_file, format = "json"):
                    list_of_dict_resp.append(json.loads(json_str))
        return list_of_dict_resp

    @classmethod
    def _get_stats(self, slices):
        list_of_time      = []
        common_mem_usage  = []
        cowrie_mem_usage  = []
        common_cpu_usage  = []
        cowrie_cpu_usage  = []
        for slice_stat in slices:
            if datetime.datetime.time(datetime.datetime.now()).hour == get_hour_from_str(slice_stat["current_time"]):
                common_mem_usage.append(slice_stat['mem_usage'])
                cowrie_mem_usage.append(slice_stat['cowrie_mem_usage'])
                common_cpu_usage.append(slice_stat['cpu_usage'])
                cowrie_cpu_usage.append(slice_stat['cowrie_cpu_usage'])
                list_of_time.append(get_minutes_from_str(slice_stat['current_time']))
        return {"common_mem_usage": common_mem_usage, "cowrie_mem_usage": cowrie_mem_usage,"common_cpu_usage": common_cpu_usage, "cowrie_cpu_usage": cowrie_cpu_usage, "time": list_of_time}
