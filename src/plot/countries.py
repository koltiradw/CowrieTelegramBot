import plotly.express as px
from collectors.logcollector import Collector
import collections
import ipscan

PATH_TO_PHOTO = 'images/countries.jpeg'

def create_hist(x_list: list, y_list: list):
    fig = px.bar(x = x_list, y = y_list, labels = dict(x = "Countries", y = "Amount of events"))
    fig.update_xaxes(type = 'category')
    fig.update_layout(uniformtext_minsize = 8, uniformtext_mode = 'hide', barmode = 'group', xaxis_tickangle = -90)
    fig.write_image(PATH_TO_PHOTO, engine = "kaleido")

def get_data(token: str, collect_obj: Collector):
    scan        = ipscan.IpScan(token)
    countries   = collections.Counter()
    keys        = ["eventid", "src_ip"]
    list_of_log = collect_obj.collect(keys)

    for log in list_of_log:
        if log['eventid'] == "cowrie.session.connect":
            scan.scan(log['src_ip'])
            countries[scan.get_country()] += 1
    list_of_countries = dict(countries).keys()
    list_of_numbers   = dict(countries).values()

    return list_of_countries, list_of_numbers

