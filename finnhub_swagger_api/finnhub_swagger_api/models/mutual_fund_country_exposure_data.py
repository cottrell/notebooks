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


class MutualFundCountryExposureData(object):
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
        'country': 'str',
        'exposure': 'float'
    }

    attribute_map = {
        'country': 'country',
        'exposure': 'exposure'
    }

    def __init__(self, country=None, exposure=None, _configuration=None):  # noqa: E501
        """MutualFundCountryExposureData - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._country = None
        self._exposure = None
        self.discriminator = None

        if country is not None:
            self.country = country
        if exposure is not None:
            self.exposure = exposure

    @property
    def country(self):
        """Gets the country of this MutualFundCountryExposureData.  # noqa: E501

        Country  # noqa: E501

        :return: The country of this MutualFundCountryExposureData.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this MutualFundCountryExposureData.

        Country  # noqa: E501

        :param country: The country of this MutualFundCountryExposureData.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def exposure(self):
        """Gets the exposure of this MutualFundCountryExposureData.  # noqa: E501

        Percent of exposure.  # noqa: E501

        :return: The exposure of this MutualFundCountryExposureData.  # noqa: E501
        :rtype: float
        """
        return self._exposure

    @exposure.setter
    def exposure(self, exposure):
        """Sets the exposure of this MutualFundCountryExposureData.

        Percent of exposure.  # noqa: E501

        :param exposure: The exposure of this MutualFundCountryExposureData.  # noqa: E501
        :type: float
        """

        self._exposure = exposure

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
        if issubclass(MutualFundCountryExposureData, dict):
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
        if not isinstance(other, MutualFundCountryExposureData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MutualFundCountryExposureData):
            return True

        return self.to_dict() != other.to_dict()