import connexion
from swagger_server.models.search_request import SearchRequest
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

    :rtype: None
    """
    if connexion.request.is_json:
        body = SearchRequest.from_dict(connexion.request.get_json())
    return 'do some magic!'


def search_items_to_items(body):
    """
    todo
    todo
    :param body: todo
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = SearchRequest.from_dict(connexion.request.get_json())
    return 'do some magic!'
