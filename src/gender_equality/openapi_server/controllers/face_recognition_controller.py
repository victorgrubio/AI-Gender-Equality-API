import connexion
import six

from openapi_server.models.detector import Detector  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.one_ofdetectorresponse_msg import OneOfdetectorresponseMsg  # noqa: E501
from openapi_server.models.one_ofresultsresponse_msg import OneOfresultsresponseMsg  # noqa: E501
from openapi_server.models.start_detector import StartDetector  # noqa: E501
from openapi_server import util


def get_results(detector=None):  # noqa: E501
    """Gets the results from the detection process

     # noqa: E501

    :param detector: 
    :type detector: dict | bytes

    :rtype: OneOfresultsresponseMsg
    """
    if connexion.request.is_json:
        detector = Detector.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def start_face_detection(start_detector=None):  # noqa: E501
    """Start the detection process

     # noqa: E501

    :param start_detector: 
    :type start_detector: dict | bytes

    :rtype: OneOfdetectorresponseMsg
    """
    if connexion.request.is_json:
        start_detector = StartDetector.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
