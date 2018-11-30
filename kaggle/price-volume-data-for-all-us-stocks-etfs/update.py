import datetime
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf

yf.pdr_override() 

stocks = ["tan"] # , "FAN"]
start = datetime.datetime(2018,5,1)
end = datetime.datetime(2018,5,12)

f = pdr.get_data_yahoo(stocks, start=start, end=end)
