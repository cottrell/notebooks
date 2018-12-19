from . import pdr, quandl
from . import lib
globals().update(lib.all_extractors)

# df = e.pdr_yahoo_price_volume.load()
# e.quandl_fred.load()
