from kuvert import cors_plugin, kuvert
from bottle import route, run, request, response
import bottle


@route("/kuvert/<id>", method=["OPTIONS", "GET"])
def kuvert_get(id):
    res = kuvert.get_kuvert(id)
    if res.success:
        return {"kuvert": res.content}
    else:
        response.status = res.error
        return {"error": res.content}


@route("/kuvert", method=["OPTIONS", "POST"])
def kuvert_save():
    data = request.json
    res= kuvert.make_kuvert(
        data["title"], data["content"], data["opening_date"], data["tag"]
    )

    if res.success:
        return {"success": True, "id": res.id}
    else:
        return {"success": False, "error": res.error}


@route("/kuvert/open", method=["OPTIONS", "GET"])
def list_open_kuvert():
    res = kuvert.get_open()
    if res.success:
        return {"success": True, "kuvert": res.kuvert}
    else:
        return {"success": False, "error": res.error}



if __name__ == "__main__":
    app = bottle.app()
    app.install(cors_plugin.EnableCors())
    app.run(port=8080, debug=True, reloader=True)

app = bottle.default_app()
