import json

class Config():
    def __init__(self, path_to_config_file: str):
        with open(path_to_config_file, 'r') as config_file:
            config_str = config_file.read()
            self.config = json.loads(config_str)
    def get_telegram_token(self) -> str:
        return self.config["telegram_token"]
    def get_virus_total_token(self) -> str:
        return self.config["virus_total_token"]
    def get_shodan_token(self) -> str:
        return self.config["shodan_token"]
    def get_ipinfo_token(self) -> str:
        return self.config["ipinfo_token"]
    def get_path_to_log_dir(self) -> str:
        return self.config["path_to_log_dir"]
    def get_path_to_download_dir(self) -> str:
        return self.config["path_to_download_dir"]
    def get_path_to_tty_dir(self) -> str:
        return self.config["path_to_tty_dir"]
    def get_list_of_valid_users(self) -> list:
        return self.config["valid_users"]
    def get_path_to_slices(self) -> str:
        return self.config["path_to_time_slices"]
    def get_path_to_cowrie(self) -> str:
        return self.config["path_to_cowrie"]
