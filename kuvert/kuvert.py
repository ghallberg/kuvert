import json
import os
from collections import namedtuple
from datetime import datetime, timedelta

import pugsql
from dotenv import load_dotenv

load_dotenv()

db_uri = os.getenv("DATABASE_URL")

# WORKING AROUND HEROKU
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

queries = pugsql.module("queries/")
queries.connect(db_uri)

MakeResult = namedtuple("MakeResult", "success error id")
ShowResult = namedtuple("ShowResult", "success error content")
OpenResult = namedtuple("OpenResult", "success error kuvert")


def get_open():
    res = list(queries.fetch_recent_open_kuvert())
    print(f"RESULT: {res}")
    return OpenResult(success=True, kuvert=res, error=None)


def get_kuvert(requested_id):
    try:
        open_res = queries.fetch_open_kuvert_by_id(id=int(requested_id))
        if open_res:
            return ShowResult(success=True, error=None, content=open_res)

        res = queries.fetch_kuvert_by_id(id=int(requested_id))
        if res:
            return ShowResult(success=True, error=None, content=res)

        return ShowResult(success=False, error=404, content="No such kuvert")
    except IOError as e:
        return ShowResult(success=False, error=500, content="dunno")


def make_kuvert(
    title, content, opening_date=datetime.now() + timedelta(weeks=1), tag=None
):
    try:
        if db_uri.startswith("post"):
            res = queries.store_kuvert(
                content=content, opening_date=opening_date, tag=tag, title=title
            )
        else:
            res = queries.store_kuvert_dev(
                content=content, opening_date=opening_date, tag=tag, title=title
            )
        print(f"RESULT: {res}")
        return MakeResult(success=True, error=None, id=res)
    except IOError as e:
        return MakeResult(success=False, error="dunno", id=None)
