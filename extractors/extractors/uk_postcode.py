from . import lib
import pandas as pd
from .lib_get_data import StandardExtractor, whoami
_mydir, _myname = lib.say_my_name()

@lib.extractor()
def get_households():
    households.maybe_get_all()
    filename = households.render_arg(None)['link']
    df = pd.read_csv(filename, compression='gzip', header=None, dtype=str)
    yield {}, df

@lib.extractor()
def get_onslookup():
    # onslookup.get_file(None)
    filename = onslookup.render_arg(None)['link']
    df = pd.read_csv(filename, compression='gzip', header=None, dtype=str)
    yield {}, df

@lib.extractor()
def get_doogal():
    doogal.maybe_get_all()
    filename = doogal.render_arg(None)['link']
    # ZIP file! very slow
    df = pd.read_csv(filename, header=None, dtype=str)
    yield {}, df

@lib.extractor()
def get_ons_postcode_dir():
    ons_postcode_dir.maybe_get_all()
    filename = ons_postcode_dir.render_arg(None)['link']
    # ZIP is multifile TODO: currently broken
    df = pd.read_csv(filename, header=None, dtype=str)
    yield {}, df

@lib.extractor()
def get_open_postcode_elevation():
    open_postcode_elevation.maybe_get_all()
    filename = open_postcode_elevation.render_arg(None)['link']
    # ZIP
    df = pd.read_csv(filename, header=None, dtype=str)
    yield {}, df

def ons_postcode_dir():
    def render_arg(arg):
        # arg is ignored
        url = 'https://ons.maps.arcgis.com/sharing/rest/content/items/8da1cb5b6daa4d72b8bbef115cf26746/data'
        filename = 'postcodes.zip'
        return dict(url=url, filename=filename, arg=arg)

    def get_args(): return None
    name = whoami()
    return StandardExtractor(name, get_args, render_arg)
ons_postcode_dir = ons_postcode_dir()

def open_postcode_elevation():
    def render_arg(arg):
        # arg is ignored
        url = 'https://www.getthedata.com/downloads/open_postcode_elevation.csv.zip'
        filename = 'postcodes.zip'
        return dict(url=url, filename=filename, arg=arg)

    def get_args(): return None
    name = whoami()
    return StandardExtractor(name, get_args, render_arg)
open_postcode_elevation = open_postcode_elevation()


# replace with this
# https://ons.maps.arcgis.com/home/search.html?t=content&q=tags%3AONS%20Postcode%20Directory&start=1&sortOrder=desc&sortField=relevance
# https://ons.maps.arcgis.com/sharing/rest/content/items/8da1cb5b6daa4d72b8bbef115cf26746/data # may 2018
def doogal():
    def render_arg(arg):
        # arg is ignored
        url = 'https://www.doogal.co.uk/files/postcodes.zip'
        filename = 'postcodes.zip'
        return dict(url=url, filename=filename, arg=arg)

    def get_args(): return None
    name = whoami()
    return StandardExtractor(name, get_args, render_arg)
doogal = doogal()


def onslookup():
    name = whoami()

    def render_arg(arg):
        # arg is ignored
        url = 'https://opendata.camden.gov.uk/api/views/tr8t-gqz7/rows.csv?accessType=DOWNLOAD'
        filename = 'onslookup.csv'
        return dict(url=url, filename=filename, arg=arg)

    def get_args(): return None
    return StandardExtractor(name, get_args, render_arg)

onslookup = onslookup()


def households():
    name = whoami()

    def render_arg(arg):
        # arg is ignored
        url = 'https://www.nomisweb.co.uk/output/census/2011/Postcode_Estimates_Table_1.csv'
        filename = 'Postcode_Estimates_Table_1.csv'
        return dict(url=url, filename=filename, arg=arg)

    def get_args(): return None
    return StandardExtractor(name, get_args, render_arg)

households = households()

