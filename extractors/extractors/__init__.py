from . import pdr, quandl, auction_co_uk, uk_postcode, uk_land_registry, edgar, imf
from . import lib
from mylib.tools import AttrDict
e = AttrDict(lib.all_extractors)

# import extractors as e
# e.e
# {'pdr_fred_meta_rate_daily': <extractors.lib.StandardExtractorAppender at 0x7f0089ca7c50>,
#  'pdr_yahoo_price_volume': <extractors.lib.StandardExtractorAppender at 0x7f006002b710>,
#  'pdr_yahoo_fx': <extractors.lib.StandardExtractorAppender at 0x7f006002b668>,
#  'quandl_fred': <extractors.lib.StandardExtractorAppender at 0x7f003c0afdd8>,
#  'quandl_oecd': <extractors.lib.StandardExtractorAppender at 0x7f003c0afd68>,
#  'quandl_ugid': <extractors.lib.StandardExtractorAppender at 0x7f003c0b4588>,
#  'quandl_lbma': <extractors.lib.StandardExtractorAppender at 0x7f003c0af9e8>,
#  'quandl_shfe': <extractors.lib.StandardExtractorAppender at 0x7f003c0afda0>,
#  'quandl_ose': <extractors.lib.StandardExtractorAppender at 0x7f003c07a908>,
#  'quandl_economist': <extractors.lib.StandardExtractorAppender at 0x7f003c07a9b0>,
#  'auction_co_uk_pastresults': <extractors.lib.StandardExtractorAppender at 0x7f003c08c208>,
#  'uk_postcode_households': <extractors.lib.StandardExtractorAppender at 0x7effeed228d0>,
#  'uk_postcode_onslookup': <extractors.lib.StandardExtractorAppender at 0x7effeed22978>,
#  'uk_postcode_doogal': <extractors.lib.StandardExtractorAppender at 0x7effeed22908>,
#  'uk_postcode_ons_postcode_dir': <extractors.lib.StandardExtractorAppender at 0x7effeed30320>,
#  'uk_postcode_open_postcode_elevation': <extractors.lib.StandardExtractorAppender at 0x7effeed302b0>,
#  'uk_land_registry_price_paid': <extractors.lib.StandardExtractorAppender at 0x7effeed39cc0>,
#  'uk_land_registry_price_paid_by_county': <extractors.lib.StandardExtractorAppender at 0x7effeed39ba8>}
#
# df = e.pdr_yahoo_price_volume.load()
# e.quandl_fred.load()
