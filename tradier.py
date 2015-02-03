import requests


endpoints = {
    'staging': 'https://sandbox.tradier.com/v1/',
    'brokerage': 'https://api.tradier.com/v1/',
    'streaming': 'https://stream.tradier.com/v1/',
    'beta': 'https://api.tradier.com/beta/', }


class Tradier(object):
    def __init__(self, token):
        self.token = token
        self.user = Tradier.User(self)
        self.options = Tradier.Options(self)
        self.watchlists = Tradier.Watchlists(self)

    def request(
        self,
        method,
        path,
        endpoint='brokerage',
        headers=None,
        params=None,
        data=None):

        headers = headers or {}
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['Accept'] = 'application/json'
        response = requests.request(
            method,
            endpoints[endpoint]+path,
            headers=headers,
            params=params,
            data=data)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    class User(object):
        def __init__(self, agent):
            self.agent = agent

        def profile(self):
            response = self.agent.request('GET', 'user/profile')
            return response

        def balances(self):
            response = self.agent.request('GET', 'user/balances')
            return response

    class Options(object):
        def __init__(self, agent):
            self.agent = agent

        def expirations(self, symbol):
            response = self.agent.request(
                'GET',
                'markets/options/expirations',
                params={'symbol': symbol})
            return response['expirations']['date']

        def chains(self, symbol, expiration):
            response = self.agent.request(
                'GET',
                'markets/options/chains',
                params={'symbol': symbol, 'expiration': expiration})
            return response['options']['option']

    class Watchlists(object):
        def __init__(self, agent):
            self.agent = agent

        def __call__(self):
            response = self.agent.request('GET', 'watchlists')
            return response['watchlists']['watchlist']

        def get(self, watchlist_id):
            response = self.agent.request(
                'GET', 'watchlists/%s' % watchlist_id)
            return response['watchlist']

        def create(self, name, *symbols):
            response = self.agent.request(
                'POST',
                'watchlists',
                params={'name': name, 'symbols': ','.join(list(symbols))})
            return response['watchlist']

        def delete(self, watchlist_id):
            response = self.agent.request(
                'DELETE', 'watchlists/%s' % watchlist_id)
            return response['watchlists']['watchlist']
