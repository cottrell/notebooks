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


class CompanyProfile2(object):
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
        'currency': 'str',
        'exchange': 'str',
        'name': 'str',
        'ticker': 'str',
        'ipo': 'date',
        'market_capitalization': 'float',
        'share_outstanding': 'float',
        'logo': 'str',
        'phone': 'str',
        'weburl': 'str',
        'finnhub_industry': 'str'
    }

    attribute_map = {
        'country': 'country',
        'currency': 'currency',
        'exchange': 'exchange',
        'name': 'name',
        'ticker': 'ticker',
        'ipo': 'ipo',
        'market_capitalization': 'marketCapitalization',
        'share_outstanding': 'shareOutstanding',
        'logo': 'logo',
        'phone': 'phone',
        'weburl': 'weburl',
        'finnhub_industry': 'finnhubIndustry'
    }

    def __init__(self, country=None, currency=None, exchange=None, name=None, ticker=None, ipo=None, market_capitalization=None, share_outstanding=None, logo=None, phone=None, weburl=None, finnhub_industry=None, _configuration=None):  # noqa: E501
        """CompanyProfile2 - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._country = None
        self._currency = None
        self._exchange = None
        self._name = None
        self._ticker = None
        self._ipo = None
        self._market_capitalization = None
        self._share_outstanding = None
        self._logo = None
        self._phone = None
        self._weburl = None
        self._finnhub_industry = None
        self.discriminator = None

        if country is not None:
            self.country = country
        if currency is not None:
            self.currency = currency
        if exchange is not None:
            self.exchange = exchange
        if name is not None:
            self.name = name
        if ticker is not None:
            self.ticker = ticker
        if ipo is not None:
            self.ipo = ipo
        if market_capitalization is not None:
            self.market_capitalization = market_capitalization
        if share_outstanding is not None:
            self.share_outstanding = share_outstanding
        if logo is not None:
            self.logo = logo
        if phone is not None:
            self.phone = phone
        if weburl is not None:
            self.weburl = weburl
        if finnhub_industry is not None:
            self.finnhub_industry = finnhub_industry

    @property
    def country(self):
        """Gets the country of this CompanyProfile2.  # noqa: E501

        Country of company's headquarter.  # noqa: E501

        :return: The country of this CompanyProfile2.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this CompanyProfile2.

        Country of company's headquarter.  # noqa: E501

        :param country: The country of this CompanyProfile2.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def currency(self):
        """Gets the currency of this CompanyProfile2.  # noqa: E501

        Currency used in company filings.  # noqa: E501

        :return: The currency of this CompanyProfile2.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this CompanyProfile2.

        Currency used in company filings.  # noqa: E501

        :param currency: The currency of this CompanyProfile2.  # noqa: E501
        :type: str
        """

        self._currency = currency

    @property
    def exchange(self):
        """Gets the exchange of this CompanyProfile2.  # noqa: E501

        Listed exchange.  # noqa: E501

        :return: The exchange of this CompanyProfile2.  # noqa: E501
        :rtype: str
        """
        return self._exchange

    @exchange.setter
    def exchange(self, exchange):
        """Sets the exchange of this CompanyProfile2.

        Listed exchange.  # noqa: E501

        :param exchange: The exchange of this CompanyProfile2.  # noqa: E501
        :type: str
        """

        self._exchange = exchange

    @property
    def name(self):
        """Gets the name of this CompanyProfile2.  # noqa: E501

        Company name.  # noqa: E501

        :return: The name of this CompanyProfile2.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CompanyProfile2.

        Company name.  # noqa: E501

        :param name: The name of this CompanyProfile2.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def ticker(self):
        """Gets the ticker of this CompanyProfile2.  # noqa: E501

        Company symbol/ticker as used on the listed exchange.  # noqa: E501

        :return: The ticker of this CompanyProfile2.  # noqa: E501
        :rtype: str
        """
        return self._ticker

    @ticker.setter
    def ticker(self, ticker):
        """Sets the ticker of this CompanyProfile2.

        Company symbol/ticker as used on the listed exchange.  # noqa: E501

        :param ticker: The ticker of this CompanyProfile2.  # noqa: E501
        :type: str
        """

        self._ticker = ticker

    @property
    def ipo(self):
        """Gets the ipo of this CompanyProfile2.  # noqa: E501

        IPO date.  # noqa: E501

        :return: The ipo of this CompanyProfile2.  # noqa: E501
        :rtype: date
        """
        return self._ipo

    @ipo.setter
    def ipo(self, ipo):
        """Sets the ipo of this CompanyProfile2.

        IPO date.  # noqa: E501

        :param ipo: The ipo of this CompanyProfile2.  # noqa: E501
        :type: date
        """

        self._ipo = ipo

    @property
    def market_capitalization(self):
        """Gets the market_capitalization of this CompanyProfile2.  # noqa: E501

        Market Capitalization.  # noqa: E501

        :return: The market_capitalization of this CompanyProfile2.  # noqa: E501
        :rtype: float
        """
        return self._market_capitalization

    @market_capitalization.setter
    def market_capitalization(self, market_capitalization):
        """Sets the market_capitalization of this CompanyProfile2.

        Market Capitalization.  # noqa: E501

        :param market_capitalization: The market_capitalization of this CompanyProfile2.  # noqa: E501
        :type: float
        """

        self._market_capitalization = market_capitalization

    @property
    def share_outstanding(self):
        """Gets the share_outstanding of this CompanyProfile2.  # noqa: E501

        Number of oustanding shares.  # noqa: E501

        :return: The share_outstanding of this CompanyProfile2.  # noqa: E501
        :rtype: float
        """
        return self._share_outstanding

    @share_outstanding.setter
    def share_outstanding(self, share_outstanding):
        """Sets the share_outstanding of this CompanyProfile2.

        Number of oustanding shares.  # noqa: E501

        :param share_outstanding: The share_outstanding of this CompanyProfile2.  # noqa: E501
        :type: float
        """

        self._share_outstanding = share_outstanding

    @property
    def logo(self):
        """Gets the logo of this CompanyProfile2.  # noqa: E501

        Logo image.  # noqa: E501

        :return: The logo of this CompanyProfile2.  # noqa: E501
        :rtype: str
        """
        return self._logo

    @logo.setter
    def logo(self, logo):
        """Sets the logo of this CompanyProfile2.

        Logo image.  # noqa: E501

        :param logo: The logo of this CompanyProfile2.  # noqa: E501
        :type: str
        """

        self._logo = logo

    @property
    def phone(self):
        """Gets the phone of this CompanyProfile2.  # noqa: E501

        Company phone number.  # noqa: E501

        :return: The phone of this CompanyProfile2.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this CompanyProfile2.

        Company phone number.  # noqa: E501

        :param phone: The phone of this CompanyProfile2.  # noqa: E501
        :type: str
        """

        self._phone = phone

    @property
    def weburl(self):
        """Gets the weburl of this CompanyProfile2.  # noqa: E501

        Company website.  # noqa: E501

        :return: The weburl of this CompanyProfile2.  # noqa: E501
        :rtype: str
        """
        return self._weburl

    @weburl.setter
    def weburl(self, weburl):
        """Sets the weburl of this CompanyProfile2.

        Company website.  # noqa: E501

        :param weburl: The weburl of this CompanyProfile2.  # noqa: E501
        :type: str
        """

        self._weburl = weburl

    @property
    def finnhub_industry(self):
        """Gets the finnhub_industry of this CompanyProfile2.  # noqa: E501

        Finnhub industry classification.  # noqa: E501

        :return: The finnhub_industry of this CompanyProfile2.  # noqa: E501
        :rtype: str
        """
        return self._finnhub_industry

    @finnhub_industry.setter
    def finnhub_industry(self, finnhub_industry):
        """Sets the finnhub_industry of this CompanyProfile2.

        Finnhub industry classification.  # noqa: E501

        :param finnhub_industry: The finnhub_industry of this CompanyProfile2.  # noqa: E501
        :type: str
        """

        self._finnhub_industry = finnhub_industry

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
        if issubclass(CompanyProfile2, dict):
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
        if not isinstance(other, CompanyProfile2):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CompanyProfile2):
            return True

        return self.to_dict() != other.to_dict()
