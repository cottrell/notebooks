#!/usr/bin/env python

import connexion
from .encoder import JSONEncoder
from flask_cors import CORS


if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'A sample API that says hello'})
    CORS(app.app)
    app.run(port=8081)
