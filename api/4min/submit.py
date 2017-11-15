#!/usr/bin/env python
""" Submit for codegen
"""

import argparse
import json
import zipfile
import yaml
import requests
import shutil


FILENAME = "codegen.zip"

def convert(specfile):
    """ convert to json
    """
    with open(specfile) as file_contents:
        data = yaml.load(file_contents.read())
        return data

def send(data):
    """ Send the swagger spec file
    """
    data = json.dumps({'spec': data, 'options': {'supportPython2': True }})
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    url = 'http://generator.swagger.io/api/gen/servers/python-flask'
    response = requests.post(url, data=data, headers=headers)
    return response.json()['link']

def retrieve(url):
    """ Retreive the codegen file and save
    """
    response = requests.get(url)
    with open(FILENAME, 'wb') as outfile:
        outfile.write(response.content)

def unzip():
    """ Unzip the codegen file
    """
    zip_ref = zipfile.ZipFile(FILENAME, 'r')
    zip_ref.extractall('.')
    zip_ref.close()
    print("Extracted in Current Directory")

def main():
    """ The main entry point
    """
    parser = argparse.ArgumentParser(description='Submit for codegen')
    parser.add_argument('-s', '--specfile', action="store", dest="specfile",
                        required=True)
    args = parser.parse_args()
    specfile = args.specfile
    data = convert(specfile)
    url = send(data)
    retrieve(url)
    unzip()

if __name__ == "__main__":
    main()
