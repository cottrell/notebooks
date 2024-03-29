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


class RecommendationTrend(object):
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
        'symbol': 'str',
        'buy': 'int',
        'hold': 'int',
        'period': 'str',
        'sell': 'int',
        'strong_buy': 'int',
        'strong_sell': 'int'
    }

    attribute_map = {
        'symbol': 'symbol',
        'buy': 'buy',
        'hold': 'hold',
        'period': 'period',
        'sell': 'sell',
        'strong_buy': 'strongBuy',
        'strong_sell': 'strongSell'
    }

    def __init__(self, symbol=None, buy=None, hold=None, period=None, sell=None, strong_buy=None, strong_sell=None, _configuration=None):  # noqa: E501
        """RecommendationTrend - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._symbol = None
        self._buy = None
        self._hold = None
        self._period = None
        self._sell = None
        self._strong_buy = None
        self._strong_sell = None
        self.discriminator = None

        if symbol is not None:
            self.symbol = symbol
        if buy is not None:
            self.buy = buy
        if hold is not None:
            self.hold = hold
        if period is not None:
            self.period = period
        if sell is not None:
            self.sell = sell
        if strong_buy is not None:
            self.strong_buy = strong_buy
        if strong_sell is not None:
            self.strong_sell = strong_sell

    @property
    def symbol(self):
        """Gets the symbol of this RecommendationTrend.  # noqa: E501

        Company symbol.  # noqa: E501

        :return: The symbol of this RecommendationTrend.  # noqa: E501
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """Sets the symbol of this RecommendationTrend.

        Company symbol.  # noqa: E501

        :param symbol: The symbol of this RecommendationTrend.  # noqa: E501
        :type: str
        """

        self._symbol = symbol

    @property
    def buy(self):
        """Gets the buy of this RecommendationTrend.  # noqa: E501

        Number of recommendations that fall into the Buy category  # noqa: E501

        :return: The buy of this RecommendationTrend.  # noqa: E501
        :rtype: int
        """
        return self._buy

    @buy.setter
    def buy(self, buy):
        """Sets the buy of this RecommendationTrend.

        Number of recommendations that fall into the Buy category  # noqa: E501

        :param buy: The buy of this RecommendationTrend.  # noqa: E501
        :type: int
        """

        self._buy = buy

    @property
    def hold(self):
        """Gets the hold of this RecommendationTrend.  # noqa: E501

        Number of recommendations that fall into the Hold category  # noqa: E501

        :return: The hold of this RecommendationTrend.  # noqa: E501
        :rtype: int
        """
        return self._hold

    @hold.setter
    def hold(self, hold):
        """Sets the hold of this RecommendationTrend.

        Number of recommendations that fall into the Hold category  # noqa: E501

        :param hold: The hold of this RecommendationTrend.  # noqa: E501
        :type: int
        """

        self._hold = hold

    @property
    def period(self):
        """Gets the period of this RecommendationTrend.  # noqa: E501

        Updated period  # noqa: E501

        :return: The period of this RecommendationTrend.  # noqa: E501
        :rtype: str
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this RecommendationTrend.

        Updated period  # noqa: E501

        :param period: The period of this RecommendationTrend.  # noqa: E501
        :type: str
        """

        self._period = period

    @property
    def sell(self):
        """Gets the sell of this RecommendationTrend.  # noqa: E501

        Number of recommendations that fall into the Sell category  # noqa: E501

        :return: The sell of this RecommendationTrend.  # noqa: E501
        :rtype: int
        """
        return self._sell

    @sell.setter
    def sell(self, sell):
        """Sets the sell of this RecommendationTrend.

        Number of recommendations that fall into the Sell category  # noqa: E501

        :param sell: The sell of this RecommendationTrend.  # noqa: E501
        :type: int
        """

        self._sell = sell

    @property
    def strong_buy(self):
        """Gets the strong_buy of this RecommendationTrend.  # noqa: E501

        Number of recommendations that fall into the Strong Buy category  # noqa: E501

        :return: The strong_buy of this RecommendationTrend.  # noqa: E501
        :rtype: int
        """
        return self._strong_buy

    @strong_buy.setter
    def strong_buy(self, strong_buy):
        """Sets the strong_buy of this RecommendationTrend.

        Number of recommendations that fall into the Strong Buy category  # noqa: E501

        :param strong_buy: The strong_buy of this RecommendationTrend.  # noqa: E501
        :type: int
        """

        self._strong_buy = strong_buy

    @property
    def strong_sell(self):
        """Gets the strong_sell of this RecommendationTrend.  # noqa: E501

        Number of recommendations that fall into the Strong Sell category  # noqa: E501

        :return: The strong_sell of this RecommendationTrend.  # noqa: E501
        :rtype: int
        """
        return self._strong_sell

    @strong_sell.setter
    def strong_sell(self, strong_sell):
        """Sets the strong_sell of this RecommendationTrend.

        Number of recommendations that fall into the Strong Sell category  # noqa: E501

        :param strong_sell: The strong_sell of this RecommendationTrend.  # noqa: E501
        :type: int
        """

        self._strong_sell = strong_sell

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
        if issubclass(RecommendationTrend, dict):
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
        if not isinstance(other, RecommendationTrend):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RecommendationTrend):
            return True

        return self.to_dict() != other.to_dict()
