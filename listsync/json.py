import requests

class JsonSource():

    def __init__(self, url, key = None, api_key = None):
        self._url = url
        self._api_key = api_key
        self._key = key

    def get_members(self):
        headers = {}
        if self._api_key:
            headers["X-Api-Key"] = self._api_key
        
        r = requests.get(self._url, headers = headers)
        data = r.json()

        if self._key is None:
            return data
        else:
            return data[self._key]

