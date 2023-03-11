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
            headers["Authorization"] = "Bearer "+self._api_key
        
        r = requests.get(self._url, headers = headers)
        data = r.json()

        key_list = (self._key or '').split('.')

        def get_key(data, key_list):
            if isinstance(data, list):
                return [get_key(d, key_list) for d in data]
            if isinstance(data, dict):
                return get_key(data.get(key_list[0], None), key_list[1:])
            return data

        data = get_key(data, key_list)

        data = [email for email in data if email]

        return data

