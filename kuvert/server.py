import kuvert
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


class EnableCors(object):
    name = "enable_cors"
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
            response.headers[
                "Access-Control-Allow-Headers"
            ] = "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"

            if bottle.request.method != "OPTIONS":
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

if __name__ == "__main__":
    app = bottle.app()
    app.install(EnableCors())
    app.run(port=8080, debug=True, reloader=True)

app = bottle.default_app()
app.install(EnableCors())
