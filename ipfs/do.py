import ipfshttpclient
# ipfsapi
if __name__ == '__main__':
    # Connect to local node
    try:
        api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        print(api)
    except ipfshttpclient.exceptions.ConnectionError as ce:
        print(str(ce))
