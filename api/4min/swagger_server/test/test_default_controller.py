# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.message import Message
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestDefaultController(BaseTestCase):
    """ DefaultController integration test stubs """

    def test_message_get(self):
        """
        Test case for message_get

        
        """
        response = self.client.open('/api/v1/message',
                                    method='GET',
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
