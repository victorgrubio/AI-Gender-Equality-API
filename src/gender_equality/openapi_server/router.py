import connexion
import traceback
from openapi_server.models.error import Error  # noqa: E501ç
from openapi_server import app_utils
from openapi_server.utils import http_utils


def get_report_detection(detector=None):  # noqa: E501
    """Gets the report from the detection process

     # noqa: E501

    :param detector:
    :type detector: dict | bytes

    :rtype: ResponseMsg
    """
    if connexion.request.is_json:
        request_json = connexion.request.get_json()
        detector_id = app_utils.add_detector(request_json['video'])
        _ = app_utils.get_detector(detector_id)
        detectors_list = app_utils.get_active_detectors()
        first_detector = app_utils.get_detector(detectors_list[0])
        if first_detector.status != "Completed":
            app_utils.start_detector(first_detector.id)
        else:
            msg = first_detector.get_report_msg()
            return http_utils.create_response(msg, 200)
    else:
        traceback.print_exc()
        return http_utils.create_server_error_response()


def detector_list():
    pass


def start_face_detection():
    try:
        if connexion.request.is_json:
            request_json = connexion.request.get_json()
            detector_id = app_utils.add_detector(request_json["video"])
            app_utils.start_detector(detector_id)
            data = {"id": detector_id}
            msg = app_utils.create_msg(data, "DETECTOR")
            return http_utils.create_response(msg, 200)
    except Exception:
        traceback.print_exc()
        return http_utils.create_server_error_response()


def get_results():
    try:
        if connexion.request.is_json:
            request_json = connexion.request.get_json()
            detector = app_utils.get_detector(request_json["id"])
            msg = detector.get_results_msg()
            return http_utils.create_response(msg, 200)
    except Exception:
        traceback.print_exc()
        return http_utils.create_server_error_response()


def get_detector_status(detector_id=None):
    try:
        detector = app_utils.get_detector(detector_id)
        data = {"status": detector.status, 
                "percentage": detector.progress}
        msg = app_utils.create_msg(data, "STATUS")
        return http_utils.create_response(msg, 200)
    except Exception:
        traceback.print_exc()
        return http_utils.create_server_error_response()
    
# def login():
#     try:
#         if connexion.request.is_json:
#             request_json = connexion.request.get_json()
#             token_dict = app_utils.login_user(
#                     request_json['username'], request_json['password'])
#             msg = app_utils.create_token_msg(token_dict)
#             return http_utils.create_response(msg, 200)
#     except Exception:
#         return http_utils.create_server_error_response()
# 
# 
# def logout():
#     pass
# 
# 
# def get_token_status():
#     pass
