import json

from urlobject import URLObject
from boto import connect_cloudfront

from . import settings
from . import paths

CACHE_FILE=paths.CACHE/'cdn.json'
def get_cache(force_rebuild=False):
    if not settings.AWS_ACCESS_KEY_ID:
        return {}
    if force_rebuild or not hasattr(get_cache, 'cache'):
        if force_rebuild or not CACHE_FILE.exists():
            CACHE_FILE.dirname().makedirs_p()
            connection = connect_cloudfront(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            distributions = connection.get_all_distributions()
            cache = {distribution.origin.dns_name: distribution.domain_name for distribution in distributions}
            with open(CACHE_FILE, 'w') as handle:
                json.dump(cache, handle)
        else:
            with open(CACHE_FILE) as handle:
                cache = json.load(handle)
        get_cache.cache = cache
    return get_cache.cache

def proxied(url):
    url = URLObject(url)
    netloc = url.netloc or settings.SERVER_NAME
    cache = get_cache()
    if netloc not in cache:
        return url
    return url.with_netloc(cache[netloc])
