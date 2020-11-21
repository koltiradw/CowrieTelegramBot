import os
import config
from hurry.filesize import size
from os.path import join, getsize
from hurry.filesize import alternative
from subprocess import check_output
import subprocess
import os.path
import time

conf = config.Config("../config.json")

def get_pid(name):
    return check_output(['pidof', name])

def du(path):
    result = ""
    try:
        result = subprocess.check_output(['du', '-sh', path]).split()[0].decode("utf-8")
    except subprocess.CalledProcessError as e:
        time.sleep(1)
        result = subprocess.check_output(['du', '-sh', path]).split()[0].decode("utf-8")
    return result
def get_number_of_files(path):
    return str(len(os.listdir(path)))

def get_cowrie_stats():
    info = ""

    info += "Overall size: " + du(conf.get_path_to_cowrie()) + "\n"
    info += "   -log dir: " + du(os.path.split(conf.get_path_to_log_dir())[0]) + " (" + get_number_of_files(os.path.split(conf.get_path_to_log_dir())[0]) + " files" + ")" + "\n"
    info += "   -downloads dir: " + du(conf.get_path_to_download_dir()) + "(" + get_number_of_files(conf.get_path_to_download_dir()) + " files" + ")" + "\n"
    info += "   -tty dir: " + du(conf.get_path_to_tty_dir()) + "(" + get_number_of_files(conf.get_path_to_tty_dir()) + " files" + ")" + "\n"

    return info

