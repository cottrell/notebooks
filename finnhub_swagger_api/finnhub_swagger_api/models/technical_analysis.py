# coding: utf-8

"""
    Finnhub API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from finnhub_swagger_api.configuration import Configuration


class TechnicalAnalysis(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'count': 'Indicator',
        'signal': 'str'
    }

    attribute_map = {
        'count': 'count',
        'signal': 'signal'
    }

    def __init__(self, count=None, signal=None, _configuration=None):  # noqa: E501
        """TechnicalAnalysis - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._count = None
        self._signal = None
        self.discriminator = None

        if count is not None:
            self.count = count
        if signal is not None:
            self.signal = signal

    @property
    def count(self):
        """Gets the count of this TechnicalAnalysis.  # noqa: E501

        Number of indicators for each signal  # noqa: E501

        :return: The count of this TechnicalAnalysis.  # noqa: E501
        :rtype: Indicator
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this TechnicalAnalysis.

        Number of indicators for each signal  # noqa: E501

        :param count: The count of this TechnicalAnalysis.  # noqa: E501
        :type: Indicator
        """

        self._count = count

    @property
    def signal(self):
        """Gets the signal of this TechnicalAnalysis.  # noqa: E501

        Aggregate Signal  # noqa: E501

        :return: The signal of this TechnicalAnalysis.  # noqa: E501
        :rtype: str
        """
        return self._signal

    @signal.setter
    def signal(self, signal):
        """Sets the signal of this TechnicalAnalysis.

        Aggregate Signal  # noqa: E501

        :param signal: The signal of this TechnicalAnalysis.  # noqa: E501
        :type: str
        """

        self._signal = signal

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(TechnicalAnalysis, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TechnicalAnalysis):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TechnicalAnalysis):
            return True

        return self.to_dict() != other.to_dict()
