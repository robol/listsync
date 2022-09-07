#
# Interface for reading and writing mailing lists data from 
# a Mailman3 server, through its REST API. 
#

import requests
from requests.auth import HTTPBasicAuth

class MailmanServer():

    def __init__(self, url, user, password):
        self._url = url
        self._user = user
        self._password = password

    def _make_request(self, path, data):
        return requests.post("%s/3.1/%s" % (self._url, path),  
            data = data,
            auth=HTTPBasicAuth(self._user, self._password)
        ).json()

    def get_members(self, list_name):
        data = self._make_request("members/find", {
            "list_id": list_name
        })
        
        return [ user["email"] for user in data["entries"] ]

    def add_member(self, list_name, email_address):
        return True

    def delete_member(self, list_name, email_address):
        return True