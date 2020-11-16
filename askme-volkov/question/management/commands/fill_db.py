from django.core.management.base import BaseCommand, CommandError
from question.models import Tag, Question, Answer
from faker import Faker
from random import choice


def add_tags():
    popular_tags = [
        "Halloween",
        "Pumpkin",
        "Spooks",
        "Very spo0ky spooks",
        "Funny Spooks",
        "Spooky Spooks",
        "2sPo0kY4u is a scammer!!1", ]
    for tag_name in popular_tags:
        Tag.objects.create(name=tag_name)


def add_questions():
    faker = Faker()
    for i in range(faker.random.randint(4, 15)):
        title = faker.sentence(5)
        content = faker.sentence(13)
        #publishing_data = faker.
        rating = faker.random.randint(-10, 27)
        all_tags = list(Tag.objects.all())
        tags = faker.random.sample(all_tags, faker.random.randint(1, 5))
        q = Question.objects.create(title=title,
                                    content=content,
                                    rating=rating, )
        q.tags.set(tags)


def add_answers():
    faker = Faker()
    for q in Question.objects.all():
        for i in range(faker.random.randint(3, 8)):
            content = faker.sentence(14)
            rating = faker.random.randint(-3, 8)
            a = Answer.objects.create(question=q,
                                      content=content,
                                      rating=rating)


class Command(BaseCommand):
    help = 'fills database with fake data'
    requires_migrations_checks = True

    def handle(self, *args, **kwargs):
        Tag.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()

        add_tags()
        add_questions()
        add_answers()

        print("Database filled")
