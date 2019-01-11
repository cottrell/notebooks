# Data Library

A bit confusing since there is name mangle.

@lib.extractor
def get_blah():
    ...

gets turned into something with name module_blah. There are various stages to getting data depending on the lib. A bit annoying right now.

To be clear the object `quandl.get_shfe` is the same as `extractors.shfe`. This is not obvious from the code.

Some extractors have effectively two stages (at the moment only two) a pull and a parse to hotcache/append and you can force to repull. I think this pattern evolved because of bulk downloads from quandl. If you have single updates it is probably easier to do something else?

And for things like yahoo, you get everything symbol by symbol, not the whole collection, so there are helpers for getting that stuff.

Remember, even if the extractors take arguments, the load will work but will load everything.

TODO: each extractor needs a create index method. This can probably just update a file. Can probably just iterate over all the extractors.

