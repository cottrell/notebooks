import connexion
from swagger_server.models.search_request import SearchRequest
from swagger_server.models.search_response import SearchResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def search_items_to_client(body):
    """
    todo
    todo
    :param body: todo
    :type body: dict | bytes

    :rtype: SearchRequest
    """
    if connexion.request.is_json:
        body = SearchResponse.from_dict(connexion.request.get_json())
    return 'do some magic!'


def search_items_to_items(body):
    """
    todo
    todo
    :param body: todo
    :type body: dict | bytes

    :rtype: SearchResponse
    """
    if connexion.request.is_json:
        body = SearchRequest.from_dict(connexion.request.get_json())
    return {'result': 'do some magic!'}

def search_client_to_client(body):
    """
    todo
    todo
    :param body: todo
    :type body: dict | bytes

    :rtype: SearchResponse
    """
    if connexion.request.is_json:
        body = SearchRequest.from_dict(connexion.request.get_json())
    return {'result': 'do some magic!'}

def search_client_to_items(body):
    """
    todo
    todo
    :param body: todo
    :type body: dict | bytes

    :rtype: SearchResponse
    """
    if connexion.request.is_json:
        body = SearchRequest.from_dict(connexion.request.get_json())
    return {'result': 'do some magic!'}
