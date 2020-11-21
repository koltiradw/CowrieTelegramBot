import ipinfo
import time

class IpScan():
    @classmethod
    def __init__(self, token: str):
        self.handler = ipinfo.getHandler(token)
        self.details = None

    @classmethod
    def scan(self, ip: str):
        self.details = self.handler.getDetails(ip)

    @classmethod
    def get_country(self) -> str:
        return self.details.country_name
