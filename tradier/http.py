import collections
import urlparse
import urllib


try:
    import requests
except ImportError:
    pass


try:
    from tornado import httpclient
    from tornado import gen
except ImportError:
    pass


class Timeout(Exception):
    pass


Response = collections.namedtuple('Response', ['code', 'headers', 'body'])


class Base(object):
    def get(self, callback, path, headers=None, params=None):
        return self.request(
            callback, 'GET', path, headers=headers, params=params)

    def post(self, callback, path, headers=None, params=None, data=''):
        return self.request(
            callback, 'POST', path, headers=headers, params=params, data=data)

    def put(self, callback, path, headers=None, params=None, data=''):
        return self.request(
            callback, 'PUT', path, headers=headers, params=params, data=data)

    def delete(self, callback, path, headers=None, params=None):
        return self.request(
            callback, 'DELETE', path, headers=headers, params=params)


class std(object):
    class Client(Base):
        def __init__(self, uri):
            self.base_uri = uri

        def response(self, response):
            return Response(
                response.status_code, response.headers, response.text)

        def request(
            self, callback, method, path,
                headers=None, params=None, data=None):
            response = requests.request(
                method, self.base_uri + path,
                headers=headers, params=params, data=data)
            return callback(self.response(response))


class tornado(object):
    class Client(Base):
        def __init__(self, uri):
            self.base_uri = uri
            self.client = httpclient.AsyncHTTPClient()

        def uri(self, path, params=None):
            uri = self.base_uri + path
            if not params:
                return uri
            return '%s?%s' % (uri, urllib.urlencode(params))

        def response(self, response):
            return Response(
                response.code, response.headers, response.body.decode('utf-8'))

        @gen.coroutine
        def request(
            self, callback, method, path,
                headers=None, params=None, data=None):

            uri = self.uri(path, params)
            request = httpclient.HTTPRequest(
                uri, method=method, headers=headers, body=data)

            try:
                response = yield self.client.fetch(request)
            except httpclient.HTTPError as e:
                if e.code == 599:
                    raise Timeout
                response = e.response

            raise gen.Return(callback(self.response(response)))


class vanilla(object):
    class Client(Base):
        def __init__(self, h, uri):
            self.h = h
            parsed = urlparse.urlsplit(uri)
            self.host = '%s://%s' % (parsed.scheme, parsed.netloc)
            self.base_path = parsed.path
