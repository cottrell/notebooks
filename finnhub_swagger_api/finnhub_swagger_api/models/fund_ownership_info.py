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


class FundOwnershipInfo(object):
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
        'share': 'int',
        'change': 'int',
        'filing_date': 'date',
        'portfolio_percent': 'float'
    }

    attribute_map = {
        'name': 'name',
        'share': 'share',
        'change': 'change',
        'filing_date': 'filingDate',
        'portfolio_percent': 'portfolioPercent'
    }

    def __init__(self, name=None, share=None, change=None, filing_date=None, portfolio_percent=None, _configuration=None):  # noqa: E501
        """FundOwnershipInfo - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._share = None
        self._change = None
        self._filing_date = None
        self._portfolio_percent = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if share is not None:
            self.share = share
        if change is not None:
            self.change = change
        if filing_date is not None:
            self.filing_date = filing_date
        if portfolio_percent is not None:
            self.portfolio_percent = portfolio_percent

    @property
    def name(self):
        """Gets the name of this FundOwnershipInfo.  # noqa: E501

        Investor's name.  # noqa: E501

        :return: The name of this FundOwnershipInfo.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this FundOwnershipInfo.

        Investor's name.  # noqa: E501

        :param name: The name of this FundOwnershipInfo.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def share(self):
        """Gets the share of this FundOwnershipInfo.  # noqa: E501

        Number of shares held by the investor.  # noqa: E501

        :return: The share of this FundOwnershipInfo.  # noqa: E501
        :rtype: int
        """
        return self._share

    @share.setter
    def share(self, share):
        """Sets the share of this FundOwnershipInfo.

        Number of shares held by the investor.  # noqa: E501

        :param share: The share of this FundOwnershipInfo.  # noqa: E501
        :type: int
        """

        self._share = share

    @property
    def change(self):
        """Gets the change of this FundOwnershipInfo.  # noqa: E501

        Number of share changed (net buy or sell) from the last period.  # noqa: E501

        :return: The change of this FundOwnershipInfo.  # noqa: E501
        :rtype: int
        """
        return self._change

    @change.setter
    def change(self, change):
        """Sets the change of this FundOwnershipInfo.

        Number of share changed (net buy or sell) from the last period.  # noqa: E501

        :param change: The change of this FundOwnershipInfo.  # noqa: E501
        :type: int
        """

        self._change = change

    @property
    def filing_date(self):
        """Gets the filing_date of this FundOwnershipInfo.  # noqa: E501

        Filing date.  # noqa: E501

        :return: The filing_date of this FundOwnershipInfo.  # noqa: E501
        :rtype: date
        """
        return self._filing_date

    @filing_date.setter
    def filing_date(self, filing_date):
        """Sets the filing_date of this FundOwnershipInfo.

        Filing date.  # noqa: E501

        :param filing_date: The filing_date of this FundOwnershipInfo.  # noqa: E501
        :type: date
        """

        self._filing_date = filing_date

    @property
    def portfolio_percent(self):
        """Gets the portfolio_percent of this FundOwnershipInfo.  # noqa: E501

        Percent of the fund's portfolio comprised of the company's share.  # noqa: E501

        :return: The portfolio_percent of this FundOwnershipInfo.  # noqa: E501
        :rtype: float
        """
        return self._portfolio_percent

    @portfolio_percent.setter
    def portfolio_percent(self, portfolio_percent):
        """Sets the portfolio_percent of this FundOwnershipInfo.

        Percent of the fund's portfolio comprised of the company's share.  # noqa: E501

        :param portfolio_percent: The portfolio_percent of this FundOwnershipInfo.  # noqa: E501
        :type: float
        """

        self._portfolio_percent = portfolio_percent

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
        if issubclass(FundOwnershipInfo, dict):
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
        if not isinstance(other, FundOwnershipInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FundOwnershipInfo):
            return True

        return self.to_dict() != other.to_dict()
