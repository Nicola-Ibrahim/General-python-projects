import datetime
from json import JSONEncoder

import dateutil.parser


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def decode_date_time(date_dict):

    # def format(value):
    #     # return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
    #     return dateutil.parser.parse(value)

    if "start" in date_dict:
        date_dict["start"] = dateutil.parser.parse(date_dict["start"])

    if "end" in date_dict:
        date_dict["end"] = dateutil.parser.parse(date_dict["end"])

    # date_dict_copy = {k: format(v) for k, v in date_dict_copy.items()}

    return date_dict
