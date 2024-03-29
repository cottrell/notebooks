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


class Quote(object):
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
        'o': 'float',
        'h': 'float',
        'l': 'float',
        'c': 'float',
        'pc': 'float',
        'd': 'float',
        'dp': 'float'
    }

    attribute_map = {
        'o': 'o',
        'h': 'h',
        'l': 'l',
        'c': 'c',
        'pc': 'pc',
        'd': 'd',
        'dp': 'dp'
    }

    def __init__(self, o=None, h=None, l=None, c=None, pc=None, d=None, dp=None, _configuration=None):  # noqa: E501
        """Quote - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._o = None
        self._h = None
        self._l = None
        self._c = None
        self._pc = None
        self._d = None
        self._dp = None
        self.discriminator = None

        if o is not None:
            self.o = o
        if h is not None:
            self.h = h
        if l is not None:
            self.l = l
        if c is not None:
            self.c = c
        if pc is not None:
            self.pc = pc
        if d is not None:
            self.d = d
        if dp is not None:
            self.dp = dp

    @property
    def o(self):
        """Gets the o of this Quote.  # noqa: E501

        Open price of the day  # noqa: E501

        :return: The o of this Quote.  # noqa: E501
        :rtype: float
        """
        return self._o

    @o.setter
    def o(self, o):
        """Sets the o of this Quote.

        Open price of the day  # noqa: E501

        :param o: The o of this Quote.  # noqa: E501
        :type: float
        """

        self._o = o

    @property
    def h(self):
        """Gets the h of this Quote.  # noqa: E501

        High price of the day  # noqa: E501

        :return: The h of this Quote.  # noqa: E501
        :rtype: float
        """
        return self._h

    @h.setter
    def h(self, h):
        """Sets the h of this Quote.

        High price of the day  # noqa: E501

        :param h: The h of this Quote.  # noqa: E501
        :type: float
        """

        self._h = h

    @property
    def l(self):
        """Gets the l of this Quote.  # noqa: E501

        Low price of the day  # noqa: E501

        :return: The l of this Quote.  # noqa: E501
        :rtype: float
        """
        return self._l

    @l.setter
    def l(self, l):
        """Sets the l of this Quote.

        Low price of the day  # noqa: E501

        :param l: The l of this Quote.  # noqa: E501
        :type: float
        """

        self._l = l

    @property
    def c(self):
        """Gets the c of this Quote.  # noqa: E501

        Current price  # noqa: E501

        :return: The c of this Quote.  # noqa: E501
        :rtype: float
        """
        return self._c

    @c.setter
    def c(self, c):
        """Sets the c of this Quote.

        Current price  # noqa: E501

        :param c: The c of this Quote.  # noqa: E501
        :type: float
        """

        self._c = c

    @property
    def pc(self):
        """Gets the pc of this Quote.  # noqa: E501

        Previous close price  # noqa: E501

        :return: The pc of this Quote.  # noqa: E501
        :rtype: float
        """
        return self._pc

    @pc.setter
    def pc(self, pc):
        """Sets the pc of this Quote.

        Previous close price  # noqa: E501

        :param pc: The pc of this Quote.  # noqa: E501
        :type: float
        """

        self._pc = pc

    @property
    def d(self):
        """Gets the d of this Quote.  # noqa: E501

        Change  # noqa: E501

        :return: The d of this Quote.  # noqa: E501
        :rtype: float
        """
        return self._d

    @d.setter
    def d(self, d):
        """Sets the d of this Quote.

        Change  # noqa: E501

        :param d: The d of this Quote.  # noqa: E501
        :type: float
        """

        self._d = d

    @property
    def dp(self):
        """Gets the dp of this Quote.  # noqa: E501

        Percent change  # noqa: E501

        :return: The dp of this Quote.  # noqa: E501
        :rtype: float
        """
        return self._dp

    @dp.setter
    def dp(self, dp):
        """Sets the dp of this Quote.

        Percent change  # noqa: E501

        :param dp: The dp of this Quote.  # noqa: E501
        :type: float
        """

        self._dp = dp

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
        if issubclass(Quote, dict):
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
        if not isinstance(other, Quote):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Quote):
            return True

        return self.to_dict() != other.to_dict()
