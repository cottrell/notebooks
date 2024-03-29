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


class EconomicCode(object):
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
        'code': 'str',
        'country': 'str',
        'name': 'str',
        'unit': 'str'
    }

    attribute_map = {
        'code': 'code',
        'country': 'country',
        'name': 'name',
        'unit': 'unit'
    }

    def __init__(self, code=None, country=None, name=None, unit=None, _configuration=None):  # noqa: E501
        """EconomicCode - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._code = None
        self._country = None
        self._name = None
        self._unit = None
        self.discriminator = None

        if code is not None:
            self.code = code
        if country is not None:
            self.country = country
        if name is not None:
            self.name = name
        if unit is not None:
            self.unit = unit

    @property
    def code(self):
        """Gets the code of this EconomicCode.  # noqa: E501

        Finnhub economic code used to get historical data  # noqa: E501

        :return: The code of this EconomicCode.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this EconomicCode.

        Finnhub economic code used to get historical data  # noqa: E501

        :param code: The code of this EconomicCode.  # noqa: E501
        :type: str
        """

        self._code = code

    @property
    def country(self):
        """Gets the country of this EconomicCode.  # noqa: E501

        Country  # noqa: E501

        :return: The country of this EconomicCode.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this EconomicCode.

        Country  # noqa: E501

        :param country: The country of this EconomicCode.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def name(self):
        """Gets the name of this EconomicCode.  # noqa: E501

        Indicator name  # noqa: E501

        :return: The name of this EconomicCode.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this EconomicCode.

        Indicator name  # noqa: E501

        :param name: The name of this EconomicCode.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def unit(self):
        """Gets the unit of this EconomicCode.  # noqa: E501

        Unit  # noqa: E501

        :return: The unit of this EconomicCode.  # noqa: E501
        :rtype: str
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """Sets the unit of this EconomicCode.

        Unit  # noqa: E501

        :param unit: The unit of this EconomicCode.  # noqa: E501
        :type: str
        """

        self._unit = unit

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
        if issubclass(EconomicCode, dict):
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
        if not isinstance(other, EconomicCode):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, EconomicCode):
            return True

        return self.to_dict() != other.to_dict()
