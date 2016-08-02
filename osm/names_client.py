# coding=utf-8
import hashlib
import json

import geonames.adapters.search

from . import caches


class GeonamesAPI(object):

    def __init__(self, **kwargs):
        super(GeonamesAPI, self).__init__()
        self.cache = kwargs.pop('cache', None)

    def send(self, query, fmt='json', out='body'):
        final_query = query

        digest = hashlib \
            .md5(final_query.encode('utf-8')) \
            .hexdigest()

        @caches.check_cache_for(self.cache, digest)
        def get_response(query):
            _USERNAME = 'bait'
            sa = geonames.adapters.search.Search(_USERNAME)
            langs = {
                'en': query
            }
            for node in sa.query(query.encode('utf-8')).max_rows(10).execute().get_xml_nodes():
                for subelement in node:
                    if 'alternateName' in subelement.tag:
                        lang = subelement.attrib['{http://www.w3.org/XML/1998/namespace}lang']
                        name = subelement.text
                        langs[lang] = name

            return json.dumps(langs)

        return get_response(final_query)

    def as_json(self, query, fmt='json', out='body'):
        return json.loads(self.send(query, fmt, out))
