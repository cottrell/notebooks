import flask
from webargs import fields
from flask_apispec import use_kwargs, marshal_with
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec

app = flask.Flask(__name__)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='stuff',
        version='v0',
        plugins=['apispec.ext.marshmallow'],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})

@app.route('/')
def welcome(**kwargs):
    return 'api is up! {}'.format(kwargs)

@app.route('/users')
@use_kwargs({'kinds': fields.Str()})
def list_pets(**kwargs):
    return "users {}".format(kwargs)

docs = FlaskApiSpec(app)
docs.register(list_pets)
# see http://0.0.0.0:5000/swagger/
