import json
import datetime


class JsonHelper(object):
    def toJson(self, toObject):
        if toObject == True:
            return json.loads(json.dumps(self.__dict__))
        else:
            return json.dumps(self.__dict__)

    def __repr__(self):
        return self.toJson()


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def safe_json(data):
    if data is None:
        return True
    elif isinstance(data, (bool, int, float)):
        return True
    elif isinstance(data, (tuple, list)):
        return all(safe_json(x) for x in data)
    elif isinstance(data, dict):
        return all(isinstance(k, str) and safe_json(v) for k, v in data.items())
    return False


def dict_to_list(data):
    if isinstance(data, dict) == False:
        return False

    dict_list = []
    for key in data.keys():
        dict_list.append(data[key])
    return dict_list
