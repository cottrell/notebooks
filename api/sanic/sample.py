from sanic import Sanic
from sanic.response import json
from sanic_openapi import swagger_blueprint, openapi_blueprint

app = Sanic()
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)
# see /swagger

@app.route("/")
async def test(request):
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
