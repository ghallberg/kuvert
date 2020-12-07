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
    result = kuvert.make_kuvert(
        data["title"], data["content"], data["opening_date"], data["tag"]
    )

    if result.success:
        return {"success": True, "id": result.id}
    else:
        return {"success": False, "error": result.error}


@route("/kuvert/open", method=["OPTIONS", "GET"])
def list_open_kuvert():
    result = kuvert.get_open()
    if result.success:
        return {"success": True, "kuvert": result.kuvert}
    else:
        return {"success": False, "error": result.error}


if __name__ == "__main__":
    app = bottle.app()
    app.install(cors_plugin.EnableCors())
    app.run(port=8080, debug=True, reloader=True)
