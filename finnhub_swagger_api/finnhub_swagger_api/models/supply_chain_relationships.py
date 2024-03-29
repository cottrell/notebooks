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


class SupplyChainRelationships(object):
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
        'data': 'list[KeyCustomersSuppliers]'
    }

    attribute_map = {
        'symbol': 'symbol',
        'data': 'data'
    }

    def __init__(self, symbol=None, data=None, _configuration=None):  # noqa: E501
        """SupplyChainRelationships - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._symbol = None
        self._data = None
        self.discriminator = None

        if symbol is not None:
            self.symbol = symbol
        if data is not None:
            self.data = data

    @property
    def symbol(self):
        """Gets the symbol of this SupplyChainRelationships.  # noqa: E501

        symbol  # noqa: E501

        :return: The symbol of this SupplyChainRelationships.  # noqa: E501
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """Sets the symbol of this SupplyChainRelationships.

        symbol  # noqa: E501

        :param symbol: The symbol of this SupplyChainRelationships.  # noqa: E501
        :type: str
        """

        self._symbol = symbol

    @property
    def data(self):
        """Gets the data of this SupplyChainRelationships.  # noqa: E501

        Key customers and suppliers.  # noqa: E501

        :return: The data of this SupplyChainRelationships.  # noqa: E501
        :rtype: list[KeyCustomersSuppliers]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this SupplyChainRelationships.

        Key customers and suppliers.  # noqa: E501

        :param data: The data of this SupplyChainRelationships.  # noqa: E501
        :type: list[KeyCustomersSuppliers]
        """

        self._data = data

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
        if issubclass(SupplyChainRelationships, dict):
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
        if not isinstance(other, SupplyChainRelationships):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SupplyChainRelationships):
            return True

        return self.to_dict() != other.to_dict()
