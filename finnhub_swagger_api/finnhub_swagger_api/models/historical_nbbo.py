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


class HistoricalNBBO(object):
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
        's': 'str',
        'skip': 'int',
        'count': 'int',
        'total': 'int',
        'av': 'list[float]',
        'a': 'list[float]',
        'ax': 'list[str]',
        'bv': 'list[float]',
        'b': 'list[float]',
        'bx': 'list[str]',
        't': 'list[int]',
        'c': 'list[list[str]]'
    }

    attribute_map = {
        's': 's',
        'skip': 'skip',
        'count': 'count',
        'total': 'total',
        'av': 'av',
        'a': 'a',
        'ax': 'ax',
        'bv': 'bv',
        'b': 'b',
        'bx': 'bx',
        't': 't',
        'c': 'c'
    }

    def __init__(self, s=None, skip=None, count=None, total=None, av=None, a=None, ax=None, bv=None, b=None, bx=None, t=None, c=None, _configuration=None):  # noqa: E501
        """HistoricalNBBO - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._s = None
        self._skip = None
        self._count = None
        self._total = None
        self._av = None
        self._a = None
        self._ax = None
        self._bv = None
        self._b = None
        self._bx = None
        self._t = None
        self._c = None
        self.discriminator = None

        if s is not None:
            self.s = s
        if skip is not None:
            self.skip = skip
        if count is not None:
            self.count = count
        if total is not None:
            self.total = total
        if av is not None:
            self.av = av
        if a is not None:
            self.a = a
        if ax is not None:
            self.ax = ax
        if bv is not None:
            self.bv = bv
        if b is not None:
            self.b = b
        if bx is not None:
            self.bx = bx
        if t is not None:
            self.t = t
        if c is not None:
            self.c = c

    @property
    def s(self):
        """Gets the s of this HistoricalNBBO.  # noqa: E501

        Symbol.  # noqa: E501

        :return: The s of this HistoricalNBBO.  # noqa: E501
        :rtype: str
        """
        return self._s

    @s.setter
    def s(self, s):
        """Sets the s of this HistoricalNBBO.

        Symbol.  # noqa: E501

        :param s: The s of this HistoricalNBBO.  # noqa: E501
        :type: str
        """

        self._s = s

    @property
    def skip(self):
        """Gets the skip of this HistoricalNBBO.  # noqa: E501

        Number of ticks skipped.  # noqa: E501

        :return: The skip of this HistoricalNBBO.  # noqa: E501
        :rtype: int
        """
        return self._skip

    @skip.setter
    def skip(self, skip):
        """Sets the skip of this HistoricalNBBO.

        Number of ticks skipped.  # noqa: E501

        :param skip: The skip of this HistoricalNBBO.  # noqa: E501
        :type: int
        """

        self._skip = skip

    @property
    def count(self):
        """Gets the count of this HistoricalNBBO.  # noqa: E501

        Number of ticks returned. If <code>count</code> < <code>limit</code>, all data for that date has been returned.  # noqa: E501

        :return: The count of this HistoricalNBBO.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this HistoricalNBBO.

        Number of ticks returned. If <code>count</code> < <code>limit</code>, all data for that date has been returned.  # noqa: E501

        :param count: The count of this HistoricalNBBO.  # noqa: E501
        :type: int
        """

        self._count = count

    @property
    def total(self):
        """Gets the total of this HistoricalNBBO.  # noqa: E501

        Total number of ticks for that date.  # noqa: E501

        :return: The total of this HistoricalNBBO.  # noqa: E501
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this HistoricalNBBO.

        Total number of ticks for that date.  # noqa: E501

        :param total: The total of this HistoricalNBBO.  # noqa: E501
        :type: int
        """

        self._total = total

    @property
    def av(self):
        """Gets the av of this HistoricalNBBO.  # noqa: E501

        List of Ask volume data.  # noqa: E501

        :return: The av of this HistoricalNBBO.  # noqa: E501
        :rtype: list[float]
        """
        return self._av

    @av.setter
    def av(self, av):
        """Sets the av of this HistoricalNBBO.

        List of Ask volume data.  # noqa: E501

        :param av: The av of this HistoricalNBBO.  # noqa: E501
        :type: list[float]
        """

        self._av = av

    @property
    def a(self):
        """Gets the a of this HistoricalNBBO.  # noqa: E501

        List of Ask price data.  # noqa: E501

        :return: The a of this HistoricalNBBO.  # noqa: E501
        :rtype: list[float]
        """
        return self._a

    @a.setter
    def a(self, a):
        """Sets the a of this HistoricalNBBO.

        List of Ask price data.  # noqa: E501

        :param a: The a of this HistoricalNBBO.  # noqa: E501
        :type: list[float]
        """

        self._a = a

    @property
    def ax(self):
        """Gets the ax of this HistoricalNBBO.  # noqa: E501

        List of venues/exchanges - Ask price. A list of exchange codes can be found <a target=\"_blank\" href=\"https://docs.google.com/spreadsheets/d/1Tj53M1svmr-hfEtbk6_NpVR1yAyGLMaH6ByYU6CG0ZY/edit?usp=sharing\",>here</a>  # noqa: E501

        :return: The ax of this HistoricalNBBO.  # noqa: E501
        :rtype: list[str]
        """
        return self._ax

    @ax.setter
    def ax(self, ax):
        """Sets the ax of this HistoricalNBBO.

        List of venues/exchanges - Ask price. A list of exchange codes can be found <a target=\"_blank\" href=\"https://docs.google.com/spreadsheets/d/1Tj53M1svmr-hfEtbk6_NpVR1yAyGLMaH6ByYU6CG0ZY/edit?usp=sharing\",>here</a>  # noqa: E501

        :param ax: The ax of this HistoricalNBBO.  # noqa: E501
        :type: list[str]
        """

        self._ax = ax

    @property
    def bv(self):
        """Gets the bv of this HistoricalNBBO.  # noqa: E501

        List of Bid volume data.  # noqa: E501

        :return: The bv of this HistoricalNBBO.  # noqa: E501
        :rtype: list[float]
        """
        return self._bv

    @bv.setter
    def bv(self, bv):
        """Sets the bv of this HistoricalNBBO.

        List of Bid volume data.  # noqa: E501

        :param bv: The bv of this HistoricalNBBO.  # noqa: E501
        :type: list[float]
        """

        self._bv = bv

    @property
    def b(self):
        """Gets the b of this HistoricalNBBO.  # noqa: E501

        List of Bid price data.  # noqa: E501

        :return: The b of this HistoricalNBBO.  # noqa: E501
        :rtype: list[float]
        """
        return self._b

    @b.setter
    def b(self, b):
        """Sets the b of this HistoricalNBBO.

        List of Bid price data.  # noqa: E501

        :param b: The b of this HistoricalNBBO.  # noqa: E501
        :type: list[float]
        """

        self._b = b

    @property
    def bx(self):
        """Gets the bx of this HistoricalNBBO.  # noqa: E501

        List of venues/exchanges - Bid price. A list of exchange codes can be found <a target=\"_blank\" href=\"https://docs.google.com/spreadsheets/d/1Tj53M1svmr-hfEtbk6_NpVR1yAyGLMaH6ByYU6CG0ZY/edit?usp=sharing\",>here</a>  # noqa: E501

        :return: The bx of this HistoricalNBBO.  # noqa: E501
        :rtype: list[str]
        """
        return self._bx

    @bx.setter
    def bx(self, bx):
        """Sets the bx of this HistoricalNBBO.

        List of venues/exchanges - Bid price. A list of exchange codes can be found <a target=\"_blank\" href=\"https://docs.google.com/spreadsheets/d/1Tj53M1svmr-hfEtbk6_NpVR1yAyGLMaH6ByYU6CG0ZY/edit?usp=sharing\",>here</a>  # noqa: E501

        :param bx: The bx of this HistoricalNBBO.  # noqa: E501
        :type: list[str]
        """

        self._bx = bx

    @property
    def t(self):
        """Gets the t of this HistoricalNBBO.  # noqa: E501

        List of timestamp in UNIX ms.  # noqa: E501

        :return: The t of this HistoricalNBBO.  # noqa: E501
        :rtype: list[int]
        """
        return self._t

    @t.setter
    def t(self, t):
        """Sets the t of this HistoricalNBBO.

        List of timestamp in UNIX ms.  # noqa: E501

        :param t: The t of this HistoricalNBBO.  # noqa: E501
        :type: list[int]
        """

        self._t = t

    @property
    def c(self):
        """Gets the c of this HistoricalNBBO.  # noqa: E501

        List of quote conditions. A comprehensive list of quote conditions code can be found <a target=\"_blank\" href=\"https://docs.google.com/spreadsheets/d/1iiA6e7Osdtai0oPMOUzgAIKXCsay89dFDmsegz6OpEg/edit?usp=sharing\">here</a>  # noqa: E501

        :return: The c of this HistoricalNBBO.  # noqa: E501
        :rtype: list[list[str]]
        """
        return self._c

    @c.setter
    def c(self, c):
        """Sets the c of this HistoricalNBBO.

        List of quote conditions. A comprehensive list of quote conditions code can be found <a target=\"_blank\" href=\"https://docs.google.com/spreadsheets/d/1iiA6e7Osdtai0oPMOUzgAIKXCsay89dFDmsegz6OpEg/edit?usp=sharing\">here</a>  # noqa: E501

        :param c: The c of this HistoricalNBBO.  # noqa: E501
        :type: list[list[str]]
        """

        self._c = c

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
        if issubclass(HistoricalNBBO, dict):
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
        if not isinstance(other, HistoricalNBBO):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, HistoricalNBBO):
            return True

        return self.to_dict() != other.to_dict()
