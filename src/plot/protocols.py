import plotly.express as px
from collectors.logcollector import Collector
import collections

PATH_TO_PHOTO = 'images/protocols.jpeg'

def create_hist(x_list: list, y_list: list):
    fig = px.bar(x = x_list, y = y_list, labels = dict(x = "Protocols", y = "Amount of events"))
    fig.update_xaxes(type='category')
    fig.update_layout(uniformtext_minsize = 8, uniformtext_mode = 'hide')
    fig.write_image(PATH_TO_PHOTO, engine = "kaleido")


def get_data(collect_obj: Collector):
    keys        = ["eventid", "protocol"]
    protocols   = collections.Counter() 
    list_of_log = collect_obj.collect(keys)
    
    for log in list_of_log:
        if log["eventid"] == "cowrie.session.connect":
            protocols[log["protocol"]] += 1

    list_of_protocols = dict(protocols).keys()
    list_of_numbers   = dict(protocols).values()

    return list_of_protocols, list_of_numbers

