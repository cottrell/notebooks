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


class MutualFundHoldings(object):
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
        'at_date': 'date',
        'number_of_holdings': 'int',
        'holdings': 'list[MutualFundHoldingsData]'
    }

    attribute_map = {
        'symbol': 'symbol',
        'at_date': 'atDate',
        'number_of_holdings': 'numberOfHoldings',
        'holdings': 'holdings'
    }

    def __init__(self, symbol=None, at_date=None, number_of_holdings=None, holdings=None, _configuration=None):  # noqa: E501
        """MutualFundHoldings - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._symbol = None
        self._at_date = None
        self._number_of_holdings = None
        self._holdings = None
        self.discriminator = None

        if symbol is not None:
            self.symbol = symbol
        if at_date is not None:
            self.at_date = at_date
        if number_of_holdings is not None:
            self.number_of_holdings = number_of_holdings
        if holdings is not None:
            self.holdings = holdings

    @property
    def symbol(self):
        """Gets the symbol of this MutualFundHoldings.  # noqa: E501

        Symbol.  # noqa: E501

        :return: The symbol of this MutualFundHoldings.  # noqa: E501
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """Sets the symbol of this MutualFundHoldings.

        Symbol.  # noqa: E501

        :param symbol: The symbol of this MutualFundHoldings.  # noqa: E501
        :type: str
        """

        self._symbol = symbol

    @property
    def at_date(self):
        """Gets the at_date of this MutualFundHoldings.  # noqa: E501

        Holdings update date.  # noqa: E501

        :return: The at_date of this MutualFundHoldings.  # noqa: E501
        :rtype: date
        """
        return self._at_date

    @at_date.setter
    def at_date(self, at_date):
        """Sets the at_date of this MutualFundHoldings.

        Holdings update date.  # noqa: E501

        :param at_date: The at_date of this MutualFundHoldings.  # noqa: E501
        :type: date
        """

        self._at_date = at_date

    @property
    def number_of_holdings(self):
        """Gets the number_of_holdings of this MutualFundHoldings.  # noqa: E501

        Number of holdings.  # noqa: E501

        :return: The number_of_holdings of this MutualFundHoldings.  # noqa: E501
        :rtype: int
        """
        return self._number_of_holdings

    @number_of_holdings.setter
    def number_of_holdings(self, number_of_holdings):
        """Sets the number_of_holdings of this MutualFundHoldings.

        Number of holdings.  # noqa: E501

        :param number_of_holdings: The number_of_holdings of this MutualFundHoldings.  # noqa: E501
        :type: int
        """

        self._number_of_holdings = number_of_holdings

    @property
    def holdings(self):
        """Gets the holdings of this MutualFundHoldings.  # noqa: E501

        Array of holdings.  # noqa: E501

        :return: The holdings of this MutualFundHoldings.  # noqa: E501
        :rtype: list[MutualFundHoldingsData]
        """
        return self._holdings

    @holdings.setter
    def holdings(self, holdings):
        """Sets the holdings of this MutualFundHoldings.

        Array of holdings.  # noqa: E501

        :param holdings: The holdings of this MutualFundHoldings.  # noqa: E501
        :type: list[MutualFundHoldingsData]
        """

        self._holdings = holdings

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
        if issubclass(MutualFundHoldings, dict):
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
        if not isinstance(other, MutualFundHoldings):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MutualFundHoldings):
            return True

        return self.to_dict() != other.to_dict()
