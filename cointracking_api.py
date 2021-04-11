import urllib
from datetime import datetime

import requests
from requests import HTTPError
from requests.cookies import cookiejar_from_dict

from settings import *

GET = 'GET'
POST = 'POST'

BASE_URL = "https://cointracking.info/ajax/"


class APIError(Exception):
    pass


class FireflyAPI:
    def __init__(self, cointracking_cookie, cointracking_cookie2):
        self.cookies = {"cointracking_cookie": cointracking_cookie, "cointracking_cookie2": cointracking_cookie2}

    def _request(self, url, data=None, method=GET, args=None):
        if args is None:
            args = {}
        args["_"] = int(datetime.now().timestamp()*1000)
        formatted_args = ('?' + urllib.parse.urlencode(args))
        r = requests.request(method=method, url=BASE_URL + url + ".php" + formatted_args, json=data, cookies=self.cookies)
        try:
            r.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == 422:
                raise APIError(r.text)
            raise e
        return r.json()['data']

    def get_monthly_balance(self):
        res = self._request('all_user_sums', args={"ct": "0_0_2"})
        return {datetime.fromtimestamp(int(l["CT_time"]["p"])).date(): float(l["CT_coin"]["p"]) for l in res[:-1]}

    def get_daily_balance(self):
        res = self._request('all_user_sums', args={"ct": "0_0_0"})
        return {datetime.fromtimestamp(int(l["CT_time"]["p"])).date(): float(l["CT_coin"]["p"]) for l in res[:-1]}


if __name__ == '__main__':
    api = FireflyAPI(COINTRACKING_COOKIE, COINTRACKING_COOKIE2)
    res = api.get_monthly_balance()
    pass
