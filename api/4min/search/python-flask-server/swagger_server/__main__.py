#!/usr/bin/env python3

import connexion
from .encoder import JSONEncoder
from flask_cors import CORS
from flask import jsonify
from flask_swagger import swagger

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'todo'})
CORS(app.app)

# does not really work well, not a reverse of codegen
@app.route("/spec")
def spec():
    return jsonify(swagger(app.app))

if __name__ == '__main__':
    app.run(server='tornado', port=8080)
