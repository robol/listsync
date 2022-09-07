import requests

class WordpressSource():

    def __init__(self, url, filter = None):
        self._url = url
        self._filter = filter

    def get_members(self):
        members = []

        r = requests.get(self._url)        
        npages = int(r.headers['X-WP-TotalPages'])

        for i in range(2, npages + 1):
            for entry in r.json():
                if self._filter is not None:
                    key, value = ( data.strip() for data in self._filter.split("=") )
                    if entry['acf'][key] != value:
                        continue
                
                # Check that the e-mail is valid
                if not '@' in entry['acf']['email']:
                    continue

                members.append(entry['acf']['email'])

            if ("?" in self._url):
                r = requests.get(self._url + "&page=%d" % i)
            else:
                r = requests.get(self._url + "?page=%d" % i)

        return members
