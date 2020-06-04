import requests

__version__ = '1.0'


class As3(object):
    def __init__(self, ip_address, port, username, password):
        self.ip = ip_address
        self.port = port
        self.username = username
        self.password = password
        self.url = f'https://{self.ip}:{self.port}/mgmt/shared/appsvcs/declare'
        self.headers = {'Content-Type': 'application/json'}

    def http_call(self, http_method, post_data, verify=False):
        """
        :param http_method: either POST or DELETE
        :param post_data: post data
        :param verify: True to verify ssl certificate
        :return: json rest api response
        """
        if http_method.lower() == 'post':
            r = requests.post(self.url, json=post_data, headers=self.headers, verify=verify,
                              auth=(self.username, self.password))
        elif http_method.lower() == 'delete':
            r = requests.delete(self.url, json=post_data, headers=self.headers, verify=verify,
                                auth=(self.username, self.password))
        else:
            raise RuntimeError(f"Invalid HTTP method: {http_method}")
        try:
            if r.status_code == 200:
                return r.json()
            else:
                raise SystemExit(f'POST call failed, HTTP RESPONSE code {r.status_code}; error {r.content}')

        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)
