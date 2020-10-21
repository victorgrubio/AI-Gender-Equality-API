import connexion
import six

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.one_ofstatusresponse_msg import OneOfstatusresponseMsg  # noqa: E501
from openapi_server import util


def get_detector_status(detector_id):  # noqa: E501
    """Posts a general message and streams messages as a result

     # noqa: E501

    :param detector_id: identification string of the target detector
    :type detector_id: str

    :rtype: OneOfstatusresponseMsg
    """
    return 'do some magic!'
