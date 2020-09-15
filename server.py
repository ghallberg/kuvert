from kuvert import cors_plugin, kuvert
from bottle import route, run, request
import bottle

@route('kuvert/<id>', method=['OPTIONS','GET'])
def kuvert_show( id="1" ):
    result = kuvert.get_kuvert(id)
    if result.success:
        return { "success": True, "content": result.content }
    else:
        return {"success": False, "error": result.error }

@route('/kuvert', method=['OPTIONS', 'POST'])
def kuvert_save():
    data = request.json
    result = kuvert.make_kuvert(
            data['title'],
            data['content'],
            data['opening_date']
    )

    if result.success:
        return { "success": True }
    else:
        return { "success": False, "error": result.error }

@route('/kuvert/<id>', method=['GET'])
def kuvert_get(id):
    res = kuvert.get_kuvert(id)
    return {"kuvert": res}


@route('/kuvert/open', method=['OPTIONS','GET'])
def list_open_kuvert():
    result = kuvert.get_open()
    if result.success:
        return { "success": True, "kuvert": result.kuvert }
    else:
        return { "success": False, "error": result.error }

app = bottle.app()
app.install(cors_plugin.EnableCors())
app.run(port=8080, debug=True, reloader=True)
