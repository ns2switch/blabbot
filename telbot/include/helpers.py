import os
from datetime import datetime, date
from .virustotal.vt import vtotal
from .storage.storage import s3bucket
from .dynamo import blabdynamo


BUCKET_NAME = os.getenv('BUCKET_NAME')
TABLE_RESULT = os.getenv('TABLE_RESULT')

def date_format(data):
    if isinstance (data, (datetime, date)) :
        return data.isoformat()
    raise TypeError ("Type %s not serializable" % type (data))
    # if type(date) is datetime:
    #    return date.strftime("%Y-%m-%d %H:%M:%S")


def channel_to_dynamo(data,channel,user):
    data_dict = data.to_dict()
    chan_dict = {'telegram' : str (data_dict['id']) + "-chan-" + str (channel),
                 'date' : str(date_format (data_dict['date'])), 'message' : data_dict['message'], 'user' : str (user),
                 'channel' : str (channel), 'mentioned' : data_dict['mentioned'], 'media' : data_dict['media'],
                 'from_id' : data_dict['from_id']}
    return chan_dict

def user_to_dynamo(data,user):
    data_dict = data.to_dict()
    chan_dict = {'telegram' : str (data_dict['id']) + "-user-" + str (user), 'date' : str(date_format(data_dict['date'])),
                 'message' : data_dict['message'], 'user' : str (user), 'media' : data_dict['media'],
                 'from_id' : data_dict['from_id']}
    return chan_dict


def log_to_dynamo(data,user):
    data_dict = data.to_dict()
    chan_dict = {'telegram' : str (data_dict['id']) + "-log-" + str (user), 'date' : str(date_format(data_dict['date'])),
                 'message' : data_dict['message'], 'user' : str (user), 'media' : data_dict['media'],
                 'from_id' : data_dict['from_id']}
    return chan_dict


def create_dict_dynamo(data,channel) :
    js = data
    meaningful_name = "" if not 'meaningful_name' in js['data']['attributes'] else str (js['data']['attributes']['meaningful_name'])
    sha256 = str (js['data']['attributes']['sha256']) if not 'meta' in js else str (
        js['meta']['file_info']['sha256'])
    type_description = str (js['data']['attributes']['type_description']) if not 'meta' in js else ""
    last_modification_date = date_format (datetime.fromtimestamp (
        js['data']['attributes']['last_modification_date'])) if not 'meta' in js else date_format (
        datetime.today ())
    last_submission_date = date_format (datetime.fromtimestamp (
        js['data']['attributes']['last_submission_date'])) if not 'meta' in js else date_format (
        datetime.fromtimestamp (js['data']['attributes']['date']))
    size = str (js['data']['attributes']['size']) if not 'meta' in js else str (js['meta']['file_info']['size'])
    times_submitted = str (js['data']['attributes']['times_submitted']) if not 'meta' in js else str (1)
    total_votes = str (js['data']['attributes']['total_votes']) if not 'meta' in js else str (0)
    type_extension = str (js['data']['attributes']['type_description']) if not 'meta' in js else str ("undefined")
    last_analysis_date = date_format (datetime.fromtimestamp (
        js['data']['attributes']['last_analysis_date'])) if not 'meta' in js else date_format (datetime.today ())
    unique_sources = str (js['data']['attributes']['unique_sources']) if not 'meta' in js else str (1)
    res_dict = {
        'sha256' : sha256,
        'type_description' : type_description,
        'last_modification_date' : last_modification_date,
        'times_submitted' : times_submitted,
        'total_votes' : total_votes,
        'size' : size,
        'type_extension' : type_extension,
        'last_submission_date' : last_submission_date,
        'last_analysis_date' : last_analysis_date,
        'unique_sources' : unique_sources,
        'meaningful_name' : meaningful_name,
        'channel': str(channel),
    }
    prev = {}
    if 'last_analysis_results' in js['data']['attributes'] :
        for key in js['data']['attributes']['last_analysis_results'] :
            virdict = {key : str (js['data']['attributes']['last_analysis_results'][key]['result'])}
            prev.update (virdict)
            res_dict.update (prev)
    else :
        for key in js['data']['attributes']['results'] :
            virdict = {key : str (js['data']['attributes']['results'][key]['result'])}
            prev.update (virdict)
            res_dict.update (prev)
    return res_dict

def analyze_and_upload(filename,channel):
    dyn = blabdynamo(TABLE_RESULT)
    data = vtotal(filename)
    infofile = data.get_hash_info()
    s3_datos = s3bucket()
    s3_datos.upload_file(filename)
    dict_dyn = create_dict_dynamo(infofile,channel)
    dyn.save(dict_dyn)
    return data.hash

