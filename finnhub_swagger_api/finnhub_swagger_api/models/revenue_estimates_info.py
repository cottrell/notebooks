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


class RevenueEstimatesInfo(object):
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
        'revenue_avg': 'float',
        'revenue_high': 'float',
        'revenue_low': 'float',
        'number_analysts': 'int',
        'period': 'date'
    }

    attribute_map = {
        'revenue_avg': 'revenueAvg',
        'revenue_high': 'revenueHigh',
        'revenue_low': 'revenueLow',
        'number_analysts': 'numberAnalysts',
        'period': 'period'
    }

    def __init__(self, revenue_avg=None, revenue_high=None, revenue_low=None, number_analysts=None, period=None, _configuration=None):  # noqa: E501
        """RevenueEstimatesInfo - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._revenue_avg = None
        self._revenue_high = None
        self._revenue_low = None
        self._number_analysts = None
        self._period = None
        self.discriminator = None

        if revenue_avg is not None:
            self.revenue_avg = revenue_avg
        if revenue_high is not None:
            self.revenue_high = revenue_high
        if revenue_low is not None:
            self.revenue_low = revenue_low
        if number_analysts is not None:
            self.number_analysts = number_analysts
        if period is not None:
            self.period = period

    @property
    def revenue_avg(self):
        """Gets the revenue_avg of this RevenueEstimatesInfo.  # noqa: E501

        Average revenue estimates including Finnhub's proprietary estimates.  # noqa: E501

        :return: The revenue_avg of this RevenueEstimatesInfo.  # noqa: E501
        :rtype: float
        """
        return self._revenue_avg

    @revenue_avg.setter
    def revenue_avg(self, revenue_avg):
        """Sets the revenue_avg of this RevenueEstimatesInfo.

        Average revenue estimates including Finnhub's proprietary estimates.  # noqa: E501

        :param revenue_avg: The revenue_avg of this RevenueEstimatesInfo.  # noqa: E501
        :type: float
        """

        self._revenue_avg = revenue_avg

    @property
    def revenue_high(self):
        """Gets the revenue_high of this RevenueEstimatesInfo.  # noqa: E501

        Highest estimate.  # noqa: E501

        :return: The revenue_high of this RevenueEstimatesInfo.  # noqa: E501
        :rtype: float
        """
        return self._revenue_high

    @revenue_high.setter
    def revenue_high(self, revenue_high):
        """Sets the revenue_high of this RevenueEstimatesInfo.

        Highest estimate.  # noqa: E501

        :param revenue_high: The revenue_high of this RevenueEstimatesInfo.  # noqa: E501
        :type: float
        """

        self._revenue_high = revenue_high

    @property
    def revenue_low(self):
        """Gets the revenue_low of this RevenueEstimatesInfo.  # noqa: E501

        Lowest estimate.  # noqa: E501

        :return: The revenue_low of this RevenueEstimatesInfo.  # noqa: E501
        :rtype: float
        """
        return self._revenue_low

    @revenue_low.setter
    def revenue_low(self, revenue_low):
        """Sets the revenue_low of this RevenueEstimatesInfo.

        Lowest estimate.  # noqa: E501

        :param revenue_low: The revenue_low of this RevenueEstimatesInfo.  # noqa: E501
        :type: float
        """

        self._revenue_low = revenue_low

    @property
    def number_analysts(self):
        """Gets the number_analysts of this RevenueEstimatesInfo.  # noqa: E501

        Number of Analysts.  # noqa: E501

        :return: The number_analysts of this RevenueEstimatesInfo.  # noqa: E501
        :rtype: int
        """
        return self._number_analysts

    @number_analysts.setter
    def number_analysts(self, number_analysts):
        """Sets the number_analysts of this RevenueEstimatesInfo.

        Number of Analysts.  # noqa: E501

        :param number_analysts: The number_analysts of this RevenueEstimatesInfo.  # noqa: E501
        :type: int
        """

        self._number_analysts = number_analysts

    @property
    def period(self):
        """Gets the period of this RevenueEstimatesInfo.  # noqa: E501

        Period.  # noqa: E501

        :return: The period of this RevenueEstimatesInfo.  # noqa: E501
        :rtype: date
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this RevenueEstimatesInfo.

        Period.  # noqa: E501

        :param period: The period of this RevenueEstimatesInfo.  # noqa: E501
        :type: date
        """

        self._period = period

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
        if issubclass(RevenueEstimatesInfo, dict):
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
        if not isinstance(other, RevenueEstimatesInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RevenueEstimatesInfo):
            return True

        return self.to_dict() != other.to_dict()