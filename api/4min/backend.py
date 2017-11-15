#!/usr/bin/env python

""" Simple swagger backend (backend.py)
"""

import argparse
import webbrowser
from flask import Flask, request

# pylint: disable=invalid-name
specfile = None
port = None
app = Flask(__name__, static_url_path='', static_folder="swagger-editor")

@app.route('/')
def root():
    """ The swagger editor entry point
    """
    return app.send_static_file('index.html')

@app.route('/editor/spec', methods=['GET', 'PUT'])
def spec():
    """ The route for swagger
    """
    if request.method == 'GET':
        try:
            with open(specfile) as file_contents:
                data = file_contents.read()
                return data
        except IOError:
            return '', 400
    if request.method == 'PUT':
        try:
            with open(specfile, 'w') as outfile:
                outfile.write(request.data.decode())
            return '', 200
        except IOError:
            return '', 400

def main():
    """ The main entry point
    """
    # pylint: disable=global-statement
    global port
    global specfile
    parser = argparse.ArgumentParser(description='Simple swagger backend')
    parser.add_argument('-p', '--port', action="store", dest="port", type=int,
                        required=True)
    parser.add_argument('-s', '--specfile', action="store", dest="specfile",
                        required=True)
    args = parser.parse_args()
    specfile = args.specfile
    port = args.port
    webbrowser.open_new('http://127.0.0.1:' + str(port))
    app.run(port=port)

if __name__ == "__main__":
    main()
