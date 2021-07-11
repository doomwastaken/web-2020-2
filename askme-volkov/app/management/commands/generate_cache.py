from django.core.management.base import BaseCommand
from django.core.cache import cache
from app.models import Tag, Profile

class Command(BaseCommand):
    def handle(self, *args, **options):
        hot_tags = Tag.objects.get_top(20)
        cache.set('hot_tags', hot_tags, 86400 + 3600)
        best_users = Profile.objects.get_top(10)
        cache.set('best_users', best_users, 86400 + 3600)
        print('Cache generated')
