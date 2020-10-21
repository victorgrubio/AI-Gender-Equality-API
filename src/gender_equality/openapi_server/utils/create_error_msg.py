# coding: utf-8

from openapi_server.models.error import Error
from openapi_server import util


class CreateErrorMsg(Error):

    def __init__(self, status=None, title=None, detail=None):
        super(CreateErrorMsg, self).__init__(
            status=status, title=title, detail=detail)

    @classmethod
    def create_error(cls, status=None, title=None, detail=None):
        return CreateErrorMsg(status=status, title=title, detail=detail)

    @classmethod
    def from_dict(cls, dikt) -> 'ResponseMsg':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The message of this Message.  # noqa: E501
        :rtype: Message
        """
        return util.deserialize_model(dikt, cls)
