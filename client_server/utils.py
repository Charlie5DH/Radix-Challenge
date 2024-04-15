from bson.objectid import ObjectId
from datetime import datetime


def convert_object_id(o):
    '''
    ObjectId values are nested within the object and are not at the top level.
    In this case, you will need to use a custom function that recursively searches for and
    converts any ObjectId values to strings.
'''
    if isinstance(o, dict):
        return {convert_object_id(k): convert_object_id(v) for k, v in o.items()}
    elif isinstance(o, list):
        return [convert_object_id(v) for v in o]
    elif isinstance(o, ObjectId):
        return str(o)
    elif isinstance(o, datetime):
        return o.isoformat()
    else:
        return o
