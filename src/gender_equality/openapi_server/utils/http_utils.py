from openapi_server.models.error import Error

from openapi_server.utils.create_response_msg import CreateResponseMsg
from openapi_server.utils.create_error_msg import CreateErrorMsg

from openapi_server.utils.message_tags import message_tags

from flask import Response


def unknownMsgError(msg):
    error_str = "Unknown message of type [{msg_tag}].".format(msg_tag=msg.tag)
    code = 404
    err = Error(code, error_str)
    r_msg = CreateResponseMsg.create_msg(
        tag=message_tags['ERROR']['tag'])
    r_msg.data = err.to_str()
    return r_msg


def create_response(msg, status_code):
    if isinstance(msg, str):
        msg_str = msg
    else:
        msg_str = msg.to_str()
    return Response(msg_str, mimetype='application/json', status=status_code)


def create_error_response(title="Error 400: to be defined",
                          detail=None,
                          status=400):
    err = CreateErrorMsg.create_error(
        status=status, title=title, detail=detail)
    return Response(err, mimetype='application/json', status=400)


def create_server_error_response(title="Error 500: to be defined",
                                 detail=None,
                                 status=500):
    err = CreateErrorMsg.create_error(
        status=status, title=title, detail=detail)
    msg_str = err.to_str()
    return Response(msg_str, mimetype='application/json', status=500)
