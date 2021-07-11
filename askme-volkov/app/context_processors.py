from django.core.cache import cache

def test(request):
    hot_tags = cache.get('hot_tags')
    best_users = cache.get('best_users')
    return {
        'hot_tags': hot_tags,
        'best_users': best_users
    }

