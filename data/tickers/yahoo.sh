#!/bin/bash
if [[ ! -e 'Yahoo Ticker Symbols - September 2017.xlsx' ]]; then
    wget http://investexcel.net/wp-content/uploads/2015/01/Yahoo-Ticker-Symbols-September-2017.zip
    unzip Yahoo-Ticker-Symbols-September-2017.zip
fi

if [[ ! -e excel_to_csv ]]; then
    python ../../excel/excel_to_csv.py 'Yahoo Ticker Symbols - September 2017.xlsx'
fi

python ./parse.py

rm -rf datapackage
mkdir -p datapackage
cp yahoo.sh parse.py yahoo_tickers.csv datapackage
cd datapackage
data init
echo THEN DO THIS: data push
