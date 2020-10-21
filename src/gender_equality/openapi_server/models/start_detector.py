# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class StartDetector(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, video=None):  # noqa: E501
        """StartDetector - a model defined in OpenAPI

        :param video: The video of this StartDetector.  # noqa: E501
        :type video: str
        """
        self.openapi_types = {
            'video': str
        }

        self.attribute_map = {
            'video': 'video'
        }

        self._video = video

    @classmethod
    def from_dict(cls, dikt) -> 'StartDetector':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The start_detector of this StartDetector.  # noqa: E501
        :rtype: StartDetector
        """
        return util.deserialize_model(dikt, cls)

    @property
    def video(self):
        """Gets the video of this StartDetector.


        :return: The video of this StartDetector.
        :rtype: str
        """
        return self._video

    @video.setter
    def video(self, video):
        """Sets the video of this StartDetector.


        :param video: The video of this StartDetector.
        :type video: str
        """
        if video is None:
            raise ValueError("Invalid value for `video`, must not be `None`")  # noqa: E501

        self._video = video
