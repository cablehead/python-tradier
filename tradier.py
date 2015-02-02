import requests


endpoints = {
    'staging': 'https://sandbox.tradier.com/v1/',
    'brokerage': 'https://api.tradier.com/v1/',
    'streaming': 'https://stream.tradier.com/v1/',
    'beta': 'https://api.tradier.com/beta/', }


class Tradier(object):
    def __init__(self, token):
        self.token = token
        self.watchlists = Tradier.Watchlists(self)

    def request(self, method, path, headers=None, params=None, data=None):
        headers = headers or {}
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['Accept'] = 'application/json'
        response = requests.request(
            method,
            endpoints['staging']+path,
            headers=headers,
            params=params,
            data=data)
        print "3"
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

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
