import flask
from webargs import fields
from flask_apispec import use_kwargs, marshal_with
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import ResourceMeta, Ref, doc, marshal_with, use_kwargs
import six
from flask import make_response
from flask_apispec.views import MethodResource

app = flask.Flask(__name__)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='stuff',
        version='v0',
        plugins=['apispec.ext.marshmallow'],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})

# simple methods

@app.route('/')
def welcome(**kwargs):
    return 'api is up! {}'.format(kwargs)

@app.route('/users')
@use_kwargs({'kinds': fields.Str()})
def list_users(**kwargs):
    return "users {}".format(kwargs)

# resources

class MethodResourceMeta(ResourceMeta, flask.views.MethodViewType):
    pass

class MethodResource(six.with_metaclass(MethodResourceMeta, flask.views.MethodView)):
    methods = None

class UserResource(MethodResource):

    def get(self, _id):
        return 'get'

    @use_kwargs({'_id': fields.Str()})
    def post(self, **kwargs):
        return Pet(**kwargs)

    @use_kwargs({'_id': fields.Str()})
    def put(self, _id, **kwargs):
        return 'put'

    def delete(self, _id):
        return make_response('delete', 204)

docs = FlaskApiSpec(app)
docs.register(list_users)
docs.register(UserResource) # this fails to be found
# see http://0.0.0.0:5000/swagger/
