# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.feed_back_form import FeedBackForm
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestFeedbackController(BaseTestCase):
    """ FeedbackController integration test stubs """

    def test_post_feedback(self):
        """
        Test case for post_feedback

        todo
        """
        body = FeedBackForm()
        response = self.client.open('/v0/feedback',
                                    method='POST',
                                    data=json.dumps(body),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
