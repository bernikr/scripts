import requests
from requests import HTTPError


class APIError(Exception):
    pass


class FireflyAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def request(self, url, data=None, method='GET'):
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.request(method=method, url=self.base_url+url, json=data, headers=headers)
        try:
            r.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == 422:
                raise APIError(r.text)
            raise e
        return r.json()['data']
