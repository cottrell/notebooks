from sanic import Sanic
from sanic.response import json
from sanic_openapi import swagger_blueprint, openapi_blueprint
from sanic_openapi import doc
from sanic_cors import CORS, cross_origin

app = Sanic()
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)
# see /swagger
CORS(app)

@app.route("/")
async def test(request):
    return json({"hello": "world"})

@app.route("/more/")
async def more(request, args, this=None):
    return json({"hello": "world"})

@app.get("/user/<user_id:int>")
@doc.summary("Fetches a user by ID")
@doc.produces({ "user": { "name": str, "id": int } })
async def get_user(request, user_id):
    return json({"bleep": "blop", "user_id": user_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
