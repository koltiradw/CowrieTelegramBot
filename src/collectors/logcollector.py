import json
import os
from splitstream import splitfile
import datetime

def get_time_from_str(timestamp: str) -> str:
    shift    = timestamp.rfind('+')
    timestamp = timestamp[:shift]
    return timestamp

def get_hour_from_str(timestamp: str) -> int:
    timestamp = get_time_from_str(timestamp)
    hour      = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f').hour
    return hour


def get_current_hour() -> int:
    return datetime.datetime.time(datetime.datetime.now()).hour

class Collector():

    @classmethod
    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file
        self.filtered_by_time_list = []
        self._filter_by_time()

    @classmethod
    def collect(self, keys: list) -> list:
        return self._filter_by_keys(keys)

    @classmethod
    def _read_log(self) -> list:
        list_of_dict_resp = []
        with open(self.path_to_file, "r") as log_file:
            for json_str in splitfile(log_file , format = 'json'):
                list_of_dict_resp.append(json.loads(json_str))
        return list_of_dict_resp

    @classmethod 
    def _filter_by_time(self):
        list_of_dict = self._read_log()
        for js in list_of_dict:
            if abs(get_current_hour() - get_hour_from_str(js["timestamp"])) == 0:
                self.filtered_by_time_list.append(js)

    @classmethod
    def _filter_by_keys(self, keys: list) -> list:
        list_of_values = []
        for js in self.filtered_by_time_list:
            tmp_dict = {}
            for key in keys:
                if js.get(key) != None:
                    tmp_dict[key] = js[key]
                    if key == "timestamp":
                        tmp_dict[key] = get_time_from_str(js[key])
            list_of_values.append(tmp_dict)
        return list_of_values
