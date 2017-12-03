import connexion
from swagger_server.models.feed_back_form import FeedBackForm
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def post_feedback(body):
    """
    todo
    todo
    :param body: todo
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = FeedBackForm.from_dict(connexion.request.get_json())
    return 'do some magic!'
