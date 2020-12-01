from question.models import Tag, Profile


def tag(request):
    return {
        'popular_tags': Tag.objects.top(5)
    }


def member(request):
    return {
        'best_members': Profile.objects.top(5)
    }