"""
test with

http://localhost:5000/pets?category=adsf&size=12
"""
from flask import Flask, make_response
from flask_restful import reqparse, abort, Api, Resource
from marshmallow import fields, Schema
from flask_apispec import use_kwargs, marshal_with
from flask_apispec.views import MethodResource
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec

app = Flask(__name__)
api = Api(app)

@app.route('/pets')
@use_kwargs({'category': fields.Str(), 'size': fields.Str()})
def get_pets(**kwargs):
    return {'something': 'here', 'size': kwargs['size'], 'category': kwargs['category']}

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='pets',
        version='v1',
        plugins=['apispec.ext.marshmallow'],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})

docs = FlaskApiSpec(app)
docs.register(get_pets)

if __name__ == '__main__':
    app.run(debug=True)
