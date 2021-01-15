import re
import urllib

import requests
from requests import HTTPError
from datetime import date
GET = 'GET'
POST = 'POST'

API_PATH = "api/v1/"


class APIError(Exception):
    pass


def format_date(d):
    if isinstance(d, str) and re.match(r'^\d{4}-(0[0-9]|1[0-2])-([012][0-9]|3[01])$', d):
        return d
    elif isinstance(d, date):
        return d.isoformat()
    raise APIError('Wrong date format, use datetime.date or YYYY-MM-DD')


class FireflyAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def _request(self, url, data=None, method=GET, args=None):
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        formatted_args = ('?' + urllib.parse.urlencode(args)) if args is not None and len(args) > 0 else ''
        r = requests.request(method=method, url=self.base_url + API_PATH + url + formatted_args, json=data,
                             headers=headers)
        try:
            r.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == 422:
                raise APIError(r.text)
            raise e
        return r.json()['data']

    def get_about(self):
        return self._request('about')

    def get_about_user(self):
        return self._request('about/user')

    def get_account_transactions(self, account_id, start=None, end=None, page=None, limit=50):
        args = {}
        if start is not None:
            args['start'] = format_date(start)
        if end is not None:
            args['end'] = format_date(end)
        args['limit'] = limit
        if page is not None:
            args['page'] = page
        return self._request('accounts/{}/transactions'.format(account_id), args=args)

    def create_transaction(self, transaction):
        return self._request('transactions', method=POST, data={'transactions': [transaction]})

    def get_accounts(self, type=None):
        args = {}
        if type is not None:
            args['type'] = type
        return self._request('accounts', args=args)
