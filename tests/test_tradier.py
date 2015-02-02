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

    print "1"
    print c.watchlists()

    print "2"
    # print c.watchlists.get('foo21')
    # print c.watchlists.delete('default')
