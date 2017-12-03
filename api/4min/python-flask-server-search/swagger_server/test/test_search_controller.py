# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.search_request import SearchRequest
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestSearchController(BaseTestCase):
    """ SearchController integration test stubs """

    def test_search_items_to_client(self):
        """
        Test case for search_items_to_client

        todo
        """
        body = SearchRequest()
        response = self.client.open('/v0/search/items_to_client',
                                    method='GET',
                                    data=json.dumps(body),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_search_items_to_items(self):
        """
        Test case for search_items_to_items

        todo
        """
        body = SearchRequest()
        response = self.client.open('/v0/search/items_to_items',
                                    method='GET',
                                    data=json.dumps(body),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
