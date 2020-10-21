# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.one_ofstatusresponse_msg import OneOfstatusresponseMsg  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDetectorController(BaseTestCase):
    """DetectorController integration test stubs"""

    def test_get_detector_status(self):
        """Test case for get_detector_status

        Posts a general message and streams messages as a result
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/gender_equality/{detector_id}/status'.format(detector_id='detector_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
