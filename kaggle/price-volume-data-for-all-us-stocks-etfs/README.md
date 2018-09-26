about 7k tickers and 3k etfs

about 1000 days max each

Interesting note about partition parquet

    # paritioned by product and name (better joins but slower read)
    ~/projects/notebooks/kaggle/price-volume-data-for-all-us-stocks-etfs $ du -sh nrows\=all/
    587M	nrows=all/
    # partitioned by produce only
    ~/projects/notebooks/kaggle/price-volume-data-for-all-us-stocks-etfs $ du -sh old
    372M	old
