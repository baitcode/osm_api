import functools
import hashlib
import os


class NotFoundError(Exception):
    def __init__(self, key, *args, **kwargs):
        super(NotFoundError, self).__init__(u'Key {} not found'.format(key))


class BaseCache(object):
    def get_key(self, value, ttl=0):
        raise NotImplementedError()

    def set(self, key, value, ttl=0):
        raise NotImplementedError()

    def get(self, key):
        raise NotImplementedError()


class NoCache(BaseCache):
    def get_key(self, value, ttl=0):
        pass

    def get(self, key):
        raise NotFoundError('Cache is disabled')

    def set(self, key, value, ttl=0):
        pass


class InMemoryCache(BaseCache):
    cache = {}

    def get_key(self, value, ttl=0):
        hasher = hashlib.md5()
        hasher.update(value)
        digest = hasher.hexdigest()
        return digest

    def get(self, key):
        if self.cache.has_key(key):
            return self.cache[key]

        raise NotFoundError(key)

    def set(self, key, value, ttl=0):
        self.cache[key] = value


class PersistentFileCache(BaseCache):
    def __init__(self, path=None):
        super(PersistentFileCache, self).__init__()
        self.path = path or 'cache/'

    def get_key(self, value, ttl=0):
        hasher = hashlib.md5()
        hasher.update(value.encode('utf-8'))
        digest = hasher.hexdigest()
        return digest

    def get(self, key):
        path = os.path.join(self.path, self.get_key(key))

        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()

        raise NotFoundError(key)

    def set(self, key, value, ttl=0):
        path = os.path.join(self.path, self.get_key(key))

        with open(path, 'w') as f:
            data = value.encode('utf-8')
            f.write(data)


def check_cache_for(cache, value, prefix = ''):
    """

    :param value: String value
    :type cache: BaseCache
    """
    key = prefix + cache.get_key(value)

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if cache is None:
                return func(*args, **kwargs)

            try:
                return cache.get(key)
            except NotFoundError:
                return_value = func(*args, **kwargs)
                cache.set(key, return_value)
                return return_value

        return wrapper

    return decorator
