import os
import time

from aldryn_django import startup


class RequestTimingMiddleware(object):
    marker = '__EXECUTION_TIME__'

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        found = False
        start = time.time()
        result = self.application(environ, start_response)
        for r in result:
            if not found and self.marker in r:
                elapsed = time.time() - start
                elapsed = '{:5.0f} ms'.format(elapsed * 1000).encode()
                r = r.replace(self.marker, elapsed)
                found = True
            yield r


application = RequestTimingMiddleware(
    startup.wsgi(path=os.path.dirname(__file__)))
