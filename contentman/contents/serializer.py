import datetime
import json

from contentful_management.resource import Link


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith("+00:00"):
                r = r[:-6] + "Z"
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, Link):
            return o.to_json()
        else:
            return super().default(o)


def dumps(data):
    return json.dumps(data, ensure_ascii=False, indent=2, cls=JSONEncoder)


def dump(data, out):
    json.dump(data, out, ensure_ascii=False, indent=2, cls=JSONEncoder)
