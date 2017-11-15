import connexion
from swagger_server.models.message import Message
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def message_get():
    """
    message_get
    Returns a greeting.

    :rtype: Message
    """
    response = Message()
    response.message = 'Hello World'
    return response
