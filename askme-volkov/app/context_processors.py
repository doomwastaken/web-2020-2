from app.models import Tag, Profile


def test(request):
    return {
        'hot_tags': Tag.objects.get_top(20),
        'best_users': Profile.objects.get_top(10)
    }

