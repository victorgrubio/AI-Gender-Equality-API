# coding: utf-8

import time

from openapi_server.models.response_msg import ResponseMsg
from openapi_server import util


class CreateResponseMsg(ResponseMsg):

    def __init__(self, tag=None, ts=None, data=None):
        super(CreateResponseMsg, self).__init__(tag=tag, ts=ts, data=data)

    @classmethod
    def create_msg(cls, tag):
        return CreateResponseMsg(tag=tag)

    @classmethod
    def from_dict(cls, dikt) -> 'ResponseMsg':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The message of this ResponseMsg.  # noqa: E501
        :rtype: Message
        """
        return util.deserialize_model(dikt, cls)

    def set_timestamp(self):
        self.ts = time.time()
