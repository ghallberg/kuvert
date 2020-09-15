import json
import pugsql
from collections import namedtuple
from datetime import datetime, timedelta

with open('config.json') as config_file:
    config_data = json.load(config_file)

DB_NAME = config_data['db']['name']

queries = pugsql.module('queries/')
queries.connect(f"sqlite:///{DB_NAME}")

MakeResult = namedtuple('MakeResult', 'success error')
ShowResult = namedtuple('ShowResult', 'success error content')
OpenResult = namedtuple('OpenResult', 'success error kuvert')

def get_open():
    res = list(queries.fetch_open_kuvert())
    return OpenResult(success=True, kuvert=res, error=None)

def get_kuvert(requested_id):
    try:
        res = queries.fetch_kuvert(id = int(requested_id));
        return ShowResult(success=True, error=None, content=res)
    except IOError as e:
        return ShowResult(success=False, error="dunno", id=None)


def make_kuvert(title, content, opening_date = datetime.now() + timedelta(weeks=1), owner = None):
    try:
        res = queries.store_kuvert(
                content = content,
                opening_date = opening_date,
                owner = owner,
                title = title
        )
        return MakeResult(success=True, error=None)
    except IOError as e:
        return MakeResult(success=False, error="dunno", id=None)

