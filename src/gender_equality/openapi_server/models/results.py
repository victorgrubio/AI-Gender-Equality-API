# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Results(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, results=None):  # noqa: E501
        """Results - a model defined in OpenAPI

        :param results: The results of this Results.  # noqa: E501
        :type results: str
        """
        self.openapi_types = {
            'results': str
        }

        self.attribute_map = {
            'results': 'results'
        }

        self._results = results

    @classmethod
    def from_dict(cls, dikt) -> 'Results':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The results of this Results.  # noqa: E501
        :rtype: Results
        """
        return util.deserialize_model(dikt, cls)

    @property
    def results(self):
        """Gets the results of this Results.


        :return: The results of this Results.
        :rtype: str
        """
        return self._results

    @results.setter
    def results(self, results):
        """Sets the results of this Results.


        :param results: The results of this Results.
        :type results: str
        """
        if results is None:
            raise ValueError("Invalid value for `results`, must not be `None`")  # noqa: E501

        self._results = results