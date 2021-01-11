from operator import itemgetter

import n26.config
import n26.api
from firefly_api import FireflyAPI
from settings import *
from datetime import date, datetime, timedelta

n26_conf = n26.config.Config(validate=False)
n26_conf.USERNAME.value = N26_USERNAME
n26_conf.PASSWORD.value = N26_PASSWORD
n26_conf.LOGIN_DATA_STORE_PATH.value = N26_LOGIN_DATA_STORE
n26_conf.MFA_TYPE.value = "app"
n26_conf.DEVICE_TOKEN.value = N26_DEVICE_TOKEN
n26_conf.validate()


def map_transaction(t, category_map):
    transaction = {
        'date': datetime.fromtimestamp(t['visibleTS']/1000).date().isoformat(),
        'amount': abs(t['amount']),
        'notes': t.get('referenceText', ''),
        'tags': ['n26 autoimport'],
        'internal_reference': t['id']
    }
    if FIREFLY_CASH_ACCOUNT_ID != -1 and t['category'] == 'micro-v2-atm':
        transaction['type'] = 'transfer'
        transaction['source_id'] = FIREFLY_N26_ACCOUNT_ID
        transaction['destination_id'] = FIREFLY_CASH_ACCOUNT_ID
        transaction['notes'] = t.get('merchantName', t.get('partnerName', ''))
        transaction['description'] = 'ATM'
    elif t['amount'] < 0:
        transaction['type'] = 'withdrawal'
        transaction['source_id'] = FIREFLY_N26_ACCOUNT_ID
        transaction['destination_name'] = t.get('merchantName', t.get('partnerName', ''))
        transaction['destination_iban'] = t.get('partnerIban', None)
        transaction['category_name'] = category_map.get(t['category'], '')
        transaction['description'] = transaction['destination_name']
    else:
        transaction['type'] = 'deposit'
        transaction['destination_id'] = FIREFLY_N26_ACCOUNT_ID
        transaction['source_name'] = t.get('merchantName', t.get('partnerName', ''))
        transaction['source_iban'] = t.get('partnerIban', None)
        transaction['description'] = transaction['source_name']
    return transaction


def import_transactions():
    n26_api = n26.api.Api(n26_conf)
    firefly_api = FireflyAPI(FIREFLY_URL, FIREFLY_TOKEN)

    print("get last transactions in Firefly")
    last_registered_transactions = firefly_api.get_account_transactions(FIREFLY_N26_ACCOUNT_ID, limit=20)
    last_registered_transactions = list(map(lambda x: x['attributes']['transactions'][0], last_registered_transactions))
    saved_ids = list(filter(lambda x: x is not None, map(itemgetter('internal_reference'), last_registered_transactions)))
    last_day = max(map(lambda x: datetime.fromisoformat(x['date']), last_registered_transactions))

    print("get latest transactions from n26")
    new_transactions = n26_api.get_transactions(from_time=int(last_day.timestamp()*1000),
                                                to_time=int(datetime.now().timestamp()*1000))
    print("get category names from n26")
    category_map = {c['id']: c['name'] for c in n26_api.get_available_categories()}

    for t in filter(lambda x: x['id'] not in saved_ids and not x['pending'], new_transactions):
        print("create new tranaction in firefly")
        t = map_transaction(t, category_map)
        firefly_api.create_transaction(t)


if __name__ == '__main__':
    import_transactions()
