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


class Company(object):
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
        'name': 'str',
        'age': 'int',
        'title': 'str',
        'since': 'str',
        'sex': 'str',
        'compensation': 'int',
        'currency': 'str'
    }

    attribute_map = {
        'name': 'name',
        'age': 'age',
        'title': 'title',
        'since': 'since',
        'sex': 'sex',
        'compensation': 'compensation',
        'currency': 'currency'
    }

    def __init__(self, name=None, age=None, title=None, since=None, sex=None, compensation=None, currency=None, _configuration=None):  # noqa: E501
        """Company - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._age = None
        self._title = None
        self._since = None
        self._sex = None
        self._compensation = None
        self._currency = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if age is not None:
            self.age = age
        if title is not None:
            self.title = title
        if since is not None:
            self.since = since
        if sex is not None:
            self.sex = sex
        if compensation is not None:
            self.compensation = compensation
        if currency is not None:
            self.currency = currency

    @property
    def name(self):
        """Gets the name of this Company.  # noqa: E501

        Executive name  # noqa: E501

        :return: The name of this Company.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Company.

        Executive name  # noqa: E501

        :param name: The name of this Company.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def age(self):
        """Gets the age of this Company.  # noqa: E501

        Age  # noqa: E501

        :return: The age of this Company.  # noqa: E501
        :rtype: int
        """
        return self._age

    @age.setter
    def age(self, age):
        """Sets the age of this Company.

        Age  # noqa: E501

        :param age: The age of this Company.  # noqa: E501
        :type: int
        """

        self._age = age

    @property
    def title(self):
        """Gets the title of this Company.  # noqa: E501

        Title  # noqa: E501

        :return: The title of this Company.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Company.

        Title  # noqa: E501

        :param title: The title of this Company.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def since(self):
        """Gets the since of this Company.  # noqa: E501

        Year appointed  # noqa: E501

        :return: The since of this Company.  # noqa: E501
        :rtype: str
        """
        return self._since

    @since.setter
    def since(self, since):
        """Sets the since of this Company.

        Year appointed  # noqa: E501

        :param since: The since of this Company.  # noqa: E501
        :type: str
        """

        self._since = since

    @property
    def sex(self):
        """Gets the sex of this Company.  # noqa: E501

        Sex  # noqa: E501

        :return: The sex of this Company.  # noqa: E501
        :rtype: str
        """
        return self._sex

    @sex.setter
    def sex(self, sex):
        """Sets the sex of this Company.

        Sex  # noqa: E501

        :param sex: The sex of this Company.  # noqa: E501
        :type: str
        """

        self._sex = sex

    @property
    def compensation(self):
        """Gets the compensation of this Company.  # noqa: E501

        Total compensation  # noqa: E501

        :return: The compensation of this Company.  # noqa: E501
        :rtype: int
        """
        return self._compensation

    @compensation.setter
    def compensation(self, compensation):
        """Sets the compensation of this Company.

        Total compensation  # noqa: E501

        :param compensation: The compensation of this Company.  # noqa: E501
        :type: int
        """

        self._compensation = compensation

    @property
    def currency(self):
        """Gets the currency of this Company.  # noqa: E501

        Compensation currency  # noqa: E501

        :return: The currency of this Company.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Company.

        Compensation currency  # noqa: E501

        :param currency: The currency of this Company.  # noqa: E501
        :type: str
        """

        self._currency = currency

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
        if issubclass(Company, dict):
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
        if not isinstance(other, Company):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Company):
            return True

        return self.to_dict() != other.to_dict()