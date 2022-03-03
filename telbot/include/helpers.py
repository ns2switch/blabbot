from datetime import datetime, date


def date_format(data):
    if isinstance (data, (datetime, date)) :
        return data.isoformat ()
    raise TypeError ("Type %s not serializable" % type (data))
    # if type(date) is datetime:
    #    return date.strftime("%Y-%m-%d %H:%M:%S")


def channel_to_dynamo(data,channel,user):
    data_dict = data.to_dict()
    chan_dict = {'telegram' : str (data_dict['id']) + "-chan-" + str (channel),
                 'date' : date_format (data_dict['date']), 'message' : data_dict['message'], 'user' : str (user),
                 'channel' : str (channel), 'mentioned' : data_dict['mentioned'], 'media' : data_dict['media'],
                 'from_id' : data_dict['from_id']}
    return chan_dict

def user_to_dynamo(data,user):
    data_dict = data.to_dict()
    chan_dict = {'telegram' : str (data_dict['id']) + "-user-" + str (user), 'date' : date_format(data_dict['date']),
                 'message' : data_dict['message'], 'user' : str (user), 'media' : data_dict['media'],
                 'from_id' : data_dict['from_id']}
    return chan_dict


def log_to_dynamo(data,user):
    data_dict = data.to_dict()
    chan_dict = {'telegram' : str (data_dict['id']) + "-log-" + str (user), 'date' : date_format(data_dict['date']),
                 'message' : data_dict['message'], 'user' : str (user), 'media' : data_dict['media'],
                 'from_id' : data_dict['from_id']}
    return chan_dict

