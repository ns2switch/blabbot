import json
from datetime import datetime

def date_format(date):
    if type(date) is datetime:
        return date.strftime("%Y-%m-%d %H:%M:%S")

def to_json(data):
    data_dict = data.to_dict()
    del data_dict['_']
    data_dict['date'] = date_format(data_dict['date'])
    data_dict['telegram'] =str(data_dict['id'])
    return data_dict