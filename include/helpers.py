import json
from datetime import datetime

def date_format(date):
    if type(date) is datetime:
        return date.strftime("%Y-%m-%d %H:%M:%S")

def channel_to_dynamo(data,channel,user):
    data_dict = data.to_dict()
    chan_dict = {}
    chan_dict['telegram'] = str (data_dict['id']) + "-chan-" + str (channel)
    chan_dict['date'] = date_format(data_dict['date'])
    chan_dict['message'] = data_dict['message']
    chan_dict['user'] = str(user)
    chan_dict['channel'] = str(channel)
    chan_dict['mentioned'] = data_dict['mentioned']
    chan_dict['media'] = data_dict['media']
    chan_dict['from_id'] = data_dict['from_id']
    return chan_dict

def user_to_dynamo(data,user):
    data_dict = data.to_dict()
    chan_dict = {}
    chan_dict['telegram'] = str (data_dict['id']) + "-user-" + str (channel)
    chan_dict['date'] = date_format(data_dict['date'])
    chan_dict['message'] = data_dict['message']
    chan_dict['user'] = str(user)
    chan_dict['media'] = data_dict['media']
    chan_dict['from_id'] = data_dict['from_id']
    return chan_dict

def log_to_dynamo(data,user):
    data_dict = data.to_dict()
    chan_dict = {}
    chan_dict['telegram'] = str (data_dict['id']) + "-log-" + str (channel)
    chan_dict['date'] = date_format(data_dict['date'])
    chan_dict['message'] = data_dict['message']
    chan_dict['user'] = str(user)
    chan_dict['media'] = data_dict['media']
    chan_dict['from_id'] = data_dict['from_id']
    return chan_dict