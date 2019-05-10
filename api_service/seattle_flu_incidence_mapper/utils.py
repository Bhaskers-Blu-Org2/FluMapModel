import json
import hashlib

from connexion import ProblemException
from flask_marshmallow import Marshmallow

ma = None


class ModelExecutionException(ProblemException):
    def __init__(self, title=None, **kwargs):
        super(ModelExecutionException, self).__init__(title=title, **kwargs)


def get_marshmallow():
    return ma


def set_marshmallow(app):
    global ma
    # Initialize Marshmallow
    ma = Marshmallow(app)
    return ma


def get_model_id(query):
    if type(query) is dict:
        pathogen = query['pathogen'] if 'pathogen' in query else ["all"]
        observed = [x for x in query['observed'] if x not in ['pathogen', 'n', 'catchment', 'positive']]
        query_json = dict(model_type=query['model_type'],
                          observed=sorted(observed, key=str.lower),
                          pathogen=pathogen)
        json_str = json.dumps(query_json, sort_keys=True, separators=(',', ':'))
    else:
        json_str = query
    m = hashlib.md5()
    m.update(json_str.encode('ascii'))
    return m.hexdigest()