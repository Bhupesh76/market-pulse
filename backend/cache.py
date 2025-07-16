from aiocache import cached

def cache_response(ttl):
    return cached(ttl=ttl)