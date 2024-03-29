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


class Development(object):
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
        '_datetime': 'str',
        'headline': 'str',
        'description': 'str',
        'url': 'str'
    }

    attribute_map = {
        'symbol': 'symbol',
        '_datetime': 'datetime',
        'headline': 'headline',
        'description': 'description',
        'url': 'url'
    }

    def __init__(self, symbol=None, _datetime=None, headline=None, description=None, url=None, _configuration=None):  # noqa: E501
        """Development - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._symbol = None
        self.__datetime = None
        self._headline = None
        self._description = None
        self._url = None
        self.discriminator = None

        if symbol is not None:
            self.symbol = symbol
        if _datetime is not None:
            self._datetime = _datetime
        if headline is not None:
            self.headline = headline
        if description is not None:
            self.description = description
        if url is not None:
            self.url = url

    @property
    def symbol(self):
        """Gets the symbol of this Development.  # noqa: E501

        Company symbol.  # noqa: E501

        :return: The symbol of this Development.  # noqa: E501
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """Sets the symbol of this Development.

        Company symbol.  # noqa: E501

        :param symbol: The symbol of this Development.  # noqa: E501
        :type: str
        """

        self._symbol = symbol

    @property
    def _datetime(self):
        """Gets the _datetime of this Development.  # noqa: E501

        Published time in <code>YYYY-MM-DD HH:MM:SS</code> format.  # noqa: E501

        :return: The _datetime of this Development.  # noqa: E501
        :rtype: str
        """
        return self.__datetime

    @_datetime.setter
    def _datetime(self, _datetime):
        """Sets the _datetime of this Development.

        Published time in <code>YYYY-MM-DD HH:MM:SS</code> format.  # noqa: E501

        :param _datetime: The _datetime of this Development.  # noqa: E501
        :type: str
        """

        self.__datetime = _datetime

    @property
    def headline(self):
        """Gets the headline of this Development.  # noqa: E501

        Development headline.  # noqa: E501

        :return: The headline of this Development.  # noqa: E501
        :rtype: str
        """
        return self._headline

    @headline.setter
    def headline(self, headline):
        """Sets the headline of this Development.

        Development headline.  # noqa: E501

        :param headline: The headline of this Development.  # noqa: E501
        :type: str
        """

        self._headline = headline

    @property
    def description(self):
        """Gets the description of this Development.  # noqa: E501

        Development description.  # noqa: E501

        :return: The description of this Development.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Development.

        Development description.  # noqa: E501

        :param description: The description of this Development.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def url(self):
        """Gets the url of this Development.  # noqa: E501

        URL.  # noqa: E501

        :return: The url of this Development.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Development.

        URL.  # noqa: E501

        :param url: The url of this Development.  # noqa: E501
        :type: str
        """

        self._url = url

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
        if issubclass(Development, dict):
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
        if not isinstance(other, Development):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Development):
            return True

        return self.to_dict() != other.to_dict()
