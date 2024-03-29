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


class ETFsCountryExposure(object):
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
        'country_exposure': 'list[ETFCountryExposureData]'
    }

    attribute_map = {
        'symbol': 'symbol',
        'country_exposure': 'countryExposure'
    }

    def __init__(self, symbol=None, country_exposure=None, _configuration=None):  # noqa: E501
        """ETFsCountryExposure - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._symbol = None
        self._country_exposure = None
        self.discriminator = None

        if symbol is not None:
            self.symbol = symbol
        if country_exposure is not None:
            self.country_exposure = country_exposure

    @property
    def symbol(self):
        """Gets the symbol of this ETFsCountryExposure.  # noqa: E501

        ETF symbol.  # noqa: E501

        :return: The symbol of this ETFsCountryExposure.  # noqa: E501
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """Sets the symbol of this ETFsCountryExposure.

        ETF symbol.  # noqa: E501

        :param symbol: The symbol of this ETFsCountryExposure.  # noqa: E501
        :type: str
        """

        self._symbol = symbol

    @property
    def country_exposure(self):
        """Gets the country_exposure of this ETFsCountryExposure.  # noqa: E501

        Array of countries and and exposure levels.  # noqa: E501

        :return: The country_exposure of this ETFsCountryExposure.  # noqa: E501
        :rtype: list[ETFCountryExposureData]
        """
        return self._country_exposure

    @country_exposure.setter
    def country_exposure(self, country_exposure):
        """Sets the country_exposure of this ETFsCountryExposure.

        Array of countries and and exposure levels.  # noqa: E501

        :param country_exposure: The country_exposure of this ETFsCountryExposure.  # noqa: E501
        :type: list[ETFCountryExposureData]
        """

        self._country_exposure = country_exposure

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
        if issubclass(ETFsCountryExposure, dict):
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
        if not isinstance(other, ETFsCountryExposure):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ETFsCountryExposure):
            return True

        return self.to_dict() != other.to_dict()
