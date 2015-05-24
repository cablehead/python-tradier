from tradier import core
from tradier import http


endpoints = {
    'staging': 'https://sandbox.tradier.com/v1/',
    'brokerage': 'https://api.tradier.com/v1/',
    'streaming': 'https://stream.tradier.com/v1/',
    'beta': 'https://api.tradier.com/beta/', }


def Tradier(token, endpoint='brokerage'):
    httpclient = http.std.Client(endpoints[endpoint])
    return core.Tradier(httpclient, token)


class vanilla(object):
    @classmethod
    def Tradier(klass, h, token, endpoint='brokerage'):
        httpclient = http.vanilla.Client(h, endpoints[endpoint])
        return core.Tradier(httpclient, token)
