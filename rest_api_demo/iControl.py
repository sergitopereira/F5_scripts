import requests
import json

__version__ = '1.1'


class IControl(object):
    def __init__(self, ip_address, port):
        self.ip = ip_address
        self.port = port
        self.headers = {
            'Content-Type': 'application/json',
            'X-F5-Auth-Token': None
        }
        self.url_base = f"https://{self.ip}:{self.port}/mgmt/tm"
        self.f5token = None
        self.username = None
        self.password = None

    def get_call(self, url, verify=False):
        """
        HTTP method GET
        :param url: resource identifier
        :param verify: True to verify ssl certificate
        :return: json rest full api response
        """
        r = requests.get(url, headers=self.headers, verify=verify)
        try:
            if r.status_code == 200:
                return r.json()
            else:
                print(url)
                raise SystemExit(f'iControl GET API call failed, HTTP RESPONSE code {r.status_code}')
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

    def post_call(self, url, post_data, verify=False):
        """
        HTTP method POST
        :param url: resource identifier
        :param post_data: post data
        :param verify: True to verify ssl certificate
        :return: json rest api response
        """
        r = requests.post(url, json.dumps(post_data), headers=self.headers, verify=verify)
        try:
            if r.status_code == 200:
                return r.json()
            else:
                raise SystemExit(f'iControl POST API call failed, HTTP RESPONSE code {r.status_code}; error {r.content}'
                                 )
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

    def patch_call(self, url, patch_data, verify):
        """
        HTTP Method PATCH
        :param url: url for api call
        :param patch_data: patch data
        :param verify: True to verify ssl certificate
        :return: json rest api
        """
        r = requests.patch(url, json.dumps(patch_data), headers=self.headers, verify=verify)
        try:
            if r.status_code == 200:
                return r.json()
            else:
                raise RuntimeError(
                    f'iControl PATCH API call failed, HTTP RESPONSE code {r.status_code}; error {r.content}')
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

    def put_call(self, url, put_data, verify):
        """
        HTTP METHOD PUT
        :param url: url for api call
        :param put_data: put data
        :param verify: True to verify ssl certificate
        :return: json rest api
        """
        try:
            r = requests.put(url, json.dumps(put_data), headers=self.headers, verify=verify)
            if r.status_code == 200:
                return r.json()
            else:
                raise SystemExit('iControl PUT API call failed,HTTP RESPONSE code {r.status_code}; error {r.content}')

        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

    def get_token(self, username, password):
        """
        :param username: F5 username
        :param password: F5 password
        :return:
        """
        self.username = username
        self.password = password
        url_auth = f"https://{self.ip}:{self.port}/mgmt/shared/authn/login"
        post_data = {
            'username': username,
            'password': password,
            'loginProviderName': 'tmos'
        }
        r = requests.post(
            url_auth, json.dumps(post_data), auth=(username, password),
            headers=self.headers, verify=False
        )
        try:
            if r.status_code == 200:
                self.f5token = r.json()['token']['token']
                self.headers['X-F5-Auth-Token'] = self.f5token
            else:
                raise SystemExit(f'was not possible to generate a token, status code = {r.status_code}')
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

    def _update_token_header(self, token):
        self.headers = {
            'Content-Type': 'application/json',
            'X-F5-Auth-Token': token
        }

    def list_virtual_servers(self, token=None):
        """
        method to list ltm virtual servers
        :param token: F5 token. not required
        :return: list of virtual servers
        """
        if token:
            self._update_token_header(token)
        url = f"{self.url_base}/ltm/virtual/"
        r = self.get_call(url)
        print(
            f'curl -sk -u {self.username}:{self.password} -H "Content-Type: application/json" -X GET {url} | jq .items')
        return r

    def get_virtual_stats(self):
        """
        Method to obtain virtual server stats
        :return: virtual server stats
        """
        resp = {}
        vips = self.list_virtual_servers()
        for vip in vips['items']:
            partition = vip['partition']
            vip = vip['name']
            print(vip)
            url = f"{self.url_base}/ltm/virtual/~{partition}~{vip}/stats"
            r = self.get_call(url)
            print(r)
            resp[vip] = r
        return resp
