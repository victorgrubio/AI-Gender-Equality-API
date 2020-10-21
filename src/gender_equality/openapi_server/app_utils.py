# -*- coding: utf-8 -*-
from openapi_server.utils.create_response_msg import CreateResponseMsg
from openapi_server.utils.message_tags import message_tags
from openapi_server import encoder
from openapi_server.server.my_app import app
# from openapi_server.db_models import User
# from flask_jwt_extended import (create_access_token, create_refresh_token,
#                                 jwt_required, jwt_refresh_token_required,
#                                 get_jwt_identity)


def create_msg(data, tag):
    msg_tag = message_tags[tag]['tag']
    msg = CreateResponseMsg.create_msg(msg_tag)
    msg.set_timestamp()
    msg.data = data
    msg_encoded = encoder.JSONEncoder().encode(msg)
    return msg_encoded


def get_active_detectors():
    return [detector for detector in app.detector_list.detector_list]

def add_detector(video):
    return app.detector_list.add_detector(video)


def get_detector(detector_id):
    return app.detector_list.get_detector(detector_id)


def get_detector_progress(detector_id):
    return app.detector_list.get_detector(detector_id).progress


def start_detector(detector_id):
    app.detector_list.start_detector(detector_id)

# 
# def create_token_msg(token_dict):
#     tag = message_tags['TOKEN']['tag']
#     msg = CreateResponseMsg.create_msg(tag)
#     msg.set_timestamp()
#     msg.data = token_dict
#     msg_encoded = encoder.JSONEncoder().encode(msg)
#     return msg_encoded
 
    # 
# def get_tokens(username, password):
#     user_identity = {"username": username, "password": password}
#     expires = datetime.timedelta(days=1)
#     access_token = create_access_token(
#             identity=user_identity, expires_delta=expires)
#     refresh_token = create_refresh_token(identity=user_identity)
#     print("Access token {}".format(access_token))
#     print("Refresh token {}".format(refresh_token))
#     return {"access_token": access_token, "refresh_token": refresh_token}

# 
# def login_user(username, password):
#     try:
#         my_user = User(username=username)
#         my_user.set_password(password)
#         user = User.query.filter_by(username=username).first()
#         if user:
#             if user.check_password(password):
#                 return get_tokens(username, password)
#             else:
#                 raise AttributeError("Password mismatch")
#         else:
#             raise AttributeError("Username {} not found".format(username))
#     except Exception:
#         print('Unexpected error : {}'.format(traceback.format_exc()))
# 
# 
# def get_users_from_db():
#     test_username = "admin1"
#     test_password = "admin1"
#     test_user = User(username=test_username)
#     test_user.set_password(test_password)
#     user = User.query.filter_by(username=test_username).first()
#     if not user:
#         app.db.session.add(test_user)
#         app.db.session.commit()
# #    get_tokens(test_username, test_password)
# #    users = User.query.all()
# #    for u in users:
# #        print(u.id, u.username)

