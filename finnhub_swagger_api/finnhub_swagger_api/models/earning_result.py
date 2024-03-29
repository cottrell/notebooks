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


class EarningResult(object):
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
        'actual': 'float',
        'estimate': 'float',
        'surprise': 'float',
        'surprise_percent': 'float',
        'period': 'date',
        'symbol': 'str'
    }

    attribute_map = {
        'actual': 'actual',
        'estimate': 'estimate',
        'surprise': 'surprise',
        'surprise_percent': 'surprisePercent',
        'period': 'period',
        'symbol': 'symbol'
    }

    def __init__(self, actual=None, estimate=None, surprise=None, surprise_percent=None, period=None, symbol=None, _configuration=None):  # noqa: E501
        """EarningResult - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._actual = None
        self._estimate = None
        self._surprise = None
        self._surprise_percent = None
        self._period = None
        self._symbol = None
        self.discriminator = None

        if actual is not None:
            self.actual = actual
        if estimate is not None:
            self.estimate = estimate
        if surprise is not None:
            self.surprise = surprise
        if surprise_percent is not None:
            self.surprise_percent = surprise_percent
        if period is not None:
            self.period = period
        if symbol is not None:
            self.symbol = symbol

    @property
    def actual(self):
        """Gets the actual of this EarningResult.  # noqa: E501

        Actual earning result.  # noqa: E501

        :return: The actual of this EarningResult.  # noqa: E501
        :rtype: float
        """
        return self._actual

    @actual.setter
    def actual(self, actual):
        """Sets the actual of this EarningResult.

        Actual earning result.  # noqa: E501

        :param actual: The actual of this EarningResult.  # noqa: E501
        :type: float
        """

        self._actual = actual

    @property
    def estimate(self):
        """Gets the estimate of this EarningResult.  # noqa: E501

        Estimated earning.  # noqa: E501

        :return: The estimate of this EarningResult.  # noqa: E501
        :rtype: float
        """
        return self._estimate

    @estimate.setter
    def estimate(self, estimate):
        """Sets the estimate of this EarningResult.

        Estimated earning.  # noqa: E501

        :param estimate: The estimate of this EarningResult.  # noqa: E501
        :type: float
        """

        self._estimate = estimate

    @property
    def surprise(self):
        """Gets the surprise of this EarningResult.  # noqa: E501

        Surprise - The difference between actual and estimate.  # noqa: E501

        :return: The surprise of this EarningResult.  # noqa: E501
        :rtype: float
        """
        return self._surprise

    @surprise.setter
    def surprise(self, surprise):
        """Sets the surprise of this EarningResult.

        Surprise - The difference between actual and estimate.  # noqa: E501

        :param surprise: The surprise of this EarningResult.  # noqa: E501
        :type: float
        """

        self._surprise = surprise

    @property
    def surprise_percent(self):
        """Gets the surprise_percent of this EarningResult.  # noqa: E501

        Surprise percent.  # noqa: E501

        :return: The surprise_percent of this EarningResult.  # noqa: E501
        :rtype: float
        """
        return self._surprise_percent

    @surprise_percent.setter
    def surprise_percent(self, surprise_percent):
        """Sets the surprise_percent of this EarningResult.

        Surprise percent.  # noqa: E501

        :param surprise_percent: The surprise_percent of this EarningResult.  # noqa: E501
        :type: float
        """

        self._surprise_percent = surprise_percent

    @property
    def period(self):
        """Gets the period of this EarningResult.  # noqa: E501

        Reported period.  # noqa: E501

        :return: The period of this EarningResult.  # noqa: E501
        :rtype: date
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this EarningResult.

        Reported period.  # noqa: E501

        :param period: The period of this EarningResult.  # noqa: E501
        :type: date
        """

        self._period = period

    @property
    def symbol(self):
        """Gets the symbol of this EarningResult.  # noqa: E501

        Company symbol.  # noqa: E501

        :return: The symbol of this EarningResult.  # noqa: E501
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """Sets the symbol of this EarningResult.

        Company symbol.  # noqa: E501

        :param symbol: The symbol of this EarningResult.  # noqa: E501
        :type: str
        """

        self._symbol = symbol

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
        if issubclass(EarningResult, dict):
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
        if not isinstance(other, EarningResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, EarningResult):
            return True

        return self.to_dict() != other.to_dict()
