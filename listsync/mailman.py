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

    def _make_request(self, path, data, json = True, method = 'POST'):
        auth = HTTPBasicAuth(self._user, self._password)

        if method == 'POST':
            data = requests.post("%s/3.1/%s" % (self._url, path),  
                data = data, auth=auth
            )
        elif method == 'DELETE':
            data = requests.delete("%s/3.1/%s" % (self._url, path),  
                data = data, auth=auth
            )
        else:
            raise RuntimeError("Unsupported method: %s" % method)

        if json:
            return data.json()
        else:
            return data.text


    def get_members(self, list_name):
        data = self._make_request("members/find", {
            "list_id": list_name
        })

        return [ user["email"] for user in data["entries"] if user['role'] == 'member' ]

    def add_member(self, list_name, email_address):
        data = self._make_request("members", {
            "list_id": list_name, 
            "subscriber": email_address, 
            "display_name": "", 
            "pre_verified": True, 
            "pre_approved": True,
            "pre_confirmed": True,
            "send_welcome_message": False
        }, json = False)

        return True

    def delete_member(self, list_name, email_address):
        data = self._make_request("lists/%s/roster/member" % list_name, {
            "emails": [ email_address ]
        }, json = False, method = 'DELETE')

        return True