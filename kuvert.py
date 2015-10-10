import json
import sqlite3
from collections import namedtuple
from datetime import datetime, timedelta
from bottle import route, run, request

config_file = open('config.json')
config_data = json.load(config_file)

DB_NAME = config_data['db']['name']

MakeResult = namedtuple('MakeResult', 'success error id')
ShowResult = namedtuple('ShowResult', 'success error content')

@route('/kuverts/<id>', method='GET')
def kuvert_show( id="1" ):
    result = get_kuvert( id )
    if result.success:
        return { "success": True, "content": result.content }
    else:
        return {"success": False, "error": result.error }

@route('/kuverts', method='POST')
def kuvert_save():
    content = request.forms.get( "content" )
    result = make_kuvert( content )
    if result.success:
        return { "success": True, "id": result.id }
    else:
        return { "success": False, "error": result.error }

def get_kuvert( id ):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT date, content FROM kuverts WHERE id = (?)''', (id))
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
                '''INSERT INTO kuverts (content,opening_date) VALUES (?, ?)''',
                (content, opening_date.isoformat()))
        conn.commit()
        return MakeResult(success=True, error=None, id=cursor.lastrowid)
    except IOError as e:
        return MakeResult(success=False, error="dunno", id=None)


run(host='localhost', port=8080, debug=True, reloader=True)
