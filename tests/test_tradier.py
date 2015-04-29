import os

import pytest

import tradier


@pytest.fixture
def token():
    return os.environ['TRADIER_ACCESS_TOKEN']


def test_core(token):
    print
    print
    c = tradier.Tradier(token)

    # print c.request('GET', 'markets/quotes', params={'symbols': 'spy'})
    # print
    # print c.request('GET', 'user/balances')
    # print
    # c.request(
    # 'GET', 'markets/fundamentals/company', params={'symbols': 'spy'})

    # print c.watchlists()

    # print c.watchlists.get('foo21')
    # print c.watchlists.delete('default')

    print
    print

    """
    print c.user.profile()
    print
    print c.user.balances()
    """

    import json

    """
    got = c.request(
        'GET',
        'markets/options/expirations',
        params={'symbol': 'AAPL'})

    print json.dumps(got, sort_keys=True, indent=4, separators=(',', ': '))
    """

    print c.options.expirations('amrs')

    got = c.options.chains('amrs', '2015-09-18')
    print json.dumps(got, sort_keys=True, indent=4, separators=(',', ': '))
