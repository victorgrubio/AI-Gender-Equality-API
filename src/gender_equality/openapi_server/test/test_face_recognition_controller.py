# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.detector import Detector  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.one_ofdetectorresponse_msg import OneOfdetectorresponseMsg  # noqa: E501
from openapi_server.models.one_ofresultsresponse_msg import OneOfresultsresponseMsg  # noqa: E501
from openapi_server.models.start_detector import StartDetector  # noqa: E501
from openapi_server.test import BaseTestCase


class TestFaceRecognitionController(BaseTestCase):
    """FaceRecognitionController integration test stubs"""

    def test_get_results(self):
        """Test case for get_results

        Gets the results from the detection process
        """
        detector = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/v1/gender_equality/results',
            method='GET',
            headers=headers,
            data=json.dumps(detector),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start_face_detection(self):
        """Test case for start_face_detection

        Start the detection process
        """
        start_detector = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/v1/gender_equality/face_detection',
            method='POST',
            headers=headers,
            data=json.dumps(start_detector),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
