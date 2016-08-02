import hashlib
import json

import requests

from . import caches


class OverpassAPI(object):
    def __init__(self, **kwargs):
        super(OverpassAPI, self).__init__()
        self.endpoint = kwargs.pop('endpoint', "http://overpass-api.de/api/interpreter")
        self.cache = kwargs.pop('cache', None)

    def send(self, query, fmt='json', out='body', prefix=''):
        final_query = u'[out:{}];{}out {};' \
            .format(fmt, query, out)

        @caches.check_cache_for(self.cache, final_query, prefix=prefix)
        def get_response(query):
            data = {
                'data': query
            }
            response = requests.get(self.endpoint, data=data)

            assert response.status_code == 200

            return response.text

        return get_response(final_query)

    def as_json(self, query, fmt='json', out='body', prefix=''):
        return json.loads(self.send(query, fmt, out, prefix=prefix))
