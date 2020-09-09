import json
import sqlite3
import pugsql
from collections import namedtuple
from datetime import datetime, timedelta
from bottle import route, run, request, response
import bottle

with open('config.json') as config_file:
    config_data = json.load(config_file)

DB_NAME = config_data['db']['name']

queries = pugsql.module('queries/')
queries.connect(f"sqlite:///{DB_NAME}")

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


MakeResult = namedtuple('MakeResult', 'success error id')
ShowResult = namedtuple('ShowResult', 'success error content')

@route('/')
def index():
    return "Hello"

@route('/kuvert/<id>', method=['OPTIONS','GET'])
def kuvert_show( id="1" ):
    result = get_kuvert( id )
    if result.success:
        return { "success": True, "content": result.content }
    else:
        return {"success": False, "error": result.error }

@route('/kuvert', method=['OPTIONS', 'POST'])
def kuvert_save():
    data = request.json
    result = make_kuvert( data['content'] )
    if result.success:
        return { "success": True, "id": result.id }
    else:
        return { "success": False, "error": result.error }

@route('/kuvert/open', method=['OPTIONS','GET'])
def list_open_kuvert():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''SELECT opening_date, content FROM kuvert WHERE opening_date <= date("now")''')
    res = [{"content": c} for c in cursor.fetchmany(100)]
    return { "success": True, "kuvert": res}

def get_kuvert( id ):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT opening_date, content FROM kuvert WHERE id = (?)''', (id))
        res = cursor.fetchone()
        conn.commit()
        return ShowResult(success=True, error=None, content=res[1])
    except IOError as e:
        return ShowResult(success=False, error="dunno", id=None)


def make_kuvert(content, opening_date = datetime.now() + timedelta(weeks=1)):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
                '''INSERT INTO kuvert (content,opening_date) VALUES (?, ?)''',
                (content, opening_date.isoformat()))
        conn.commit()
        return MakeResult(success=True, error=None, id=cursor.lastrowid)
    except IOError as e:
        return MakeResult(success=False, error="dunno", id=None)


app = bottle.app()
app.install(EnableCors())
app.run(port=8080, debug=True, reloader=True)
