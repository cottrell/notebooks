from __future__ import print_function
import datetime
import argh
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import joblib
from cryptography.fernet import Fernet
import os
import json
memory = joblib.Memory('joblib_cache_temp', verbose=1)
_memory = joblib.Memory('joblib_cache_persist', verbose=1)

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def get_service():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('gmail', 'v1', http=creds.authorize(Http()))

try:
    service
except NameError as e:
    service = get_service()

@memory.cache
def _list(query, maxResults=500):
    # I think it is limited to 500
    # returns dict_keys(['messages', 'nextPageToken', 'resultSizeEstimate'])
    return service.users().messages().list(userId='me', q=query, maxResults=maxResults).execute()

@memory.cache
def get(_id, format='metadata'):
    return service.users().messages().get(userId='me', id=_id, format=format).execute()

@memory.cache
def search(query, maxResults=500, format='metadata'):
    """
    examples:
    r = search('blahblah')
    [x['value'] for y in r for x in y['payload']['headers'] if x['name'] == 'From']
    """
    r = _list(query, maxResults=maxResults)
    results = list()
    # ['messages', 'nextPageToken', 'resultSizeEstimate'] # if you want to paginate check for nextPageToken and call back on that
    for x in r['messages']:
        results.append(get(x['id'], format=format))
    return results

key = json.load(open(os.path.join(os.path.expanduser('~/.cred/weak/cred.json'))))['key'].encode()
_from_list = Fernet(key).decrypt(open('./enc.txt').read().encode()).decode().strip().split()

def search_A(after=datetime.date.today()):
    # this will be persisted by the above stuff
    if type(after) is str:
        after = datetime.datetime.strptime(after, '%Y-%m-%d').date()
    before = after + datetime.timedelta(days=1)
    query = 'from: ' + ' OR '.join(_from_list)
    query += ' after:{} before:{}'.format(after, before)
    # print(query)
    return search(query, format='full')

def n_days_back(n):
    date = datetime.date.today()
    res = list()
    for i in range(n):
        date -= datetime.timedelta(days=1)
        try:
            res.append(search_A(after=date))
        except Exception as e:
            print('could not search_A for {} ... not sure if this means search result is empty'.format(date))
    return res

# users().messages().list(userId='me', q='after:2018-11-19 before:2018-11-20').execute()

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

if __name__ == '__main__':
    argh.dispatch_command(search_A)
