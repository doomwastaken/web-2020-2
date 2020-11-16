from app.models import Question, Author, Answer, Tag
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from faker import Faker
import os, random
from django.utils import timezone

f = Faker()

class Command(BaseCommand):

    USERS_COUNT = 10
    TAGS_COUNT = 10
    QUESTIONS_COUNT_FOR_ONE_USER = 5
    MAX_ANSWERS_FOR_ONE_QUESTION = 5
    TAGS_COUNT_FOR_ONE_QUESTION = 3

 #   def add_arguments(self, parser):
 #       parser.add_argument('--authors', type=int)
 #       parser.add_argument('--questions', type=int)
 #       parser.add_argument('--answers', type=int)
 #       parser.add_argument('--tags', type=int)

    def fill_authors(self):
        for i in range(self.USERS_COUNT):
            u = User(username=f.name())
            u.email = f.email()
            u.first_name = f.first_name()
            u.save()
            Author.objects.create(
                avatar=random.choice(os.listdir("/home/vk/tp/web-2020-2/Media")),
                user=u,
                rating=f.random_int(min=-100, max=100),
            )
        pass

    def fill_questions(self):
        for i in range(self.QUESTIONS_COUNT_FOR_ONE_USER):
            a_ids = Author.objects.values_list('id')
            t_ids = Tag.objects.values_list('id')
            u=Author.objects.get(id=random.choice(a_ids)[0])
            q = Question.objects.create(
                rating=f.random_int(min=-100, max=100),
                author=u,
                title=f.sentence()[0:10],
                content=f.text(),
                date_added=timezone.now(),
            )

          # for j in range(f.random_int(min=2, max=6)):
                #t=Tag.objects.get(id=random.choice(t_ids)[0])
                #t.rating = t.rating + 1
                #t.save()
               # q.tags.add(t)
           # q.save()
        pass

    def fill_answers(self):
        for i in range(self.MAX_ANSWERS_FOR_ONE_QUESTION):
            a_ids = Author.objects.values_list('id')
            u = Author.objects.get(id=random.choice(a_ids)[0])
            q_ids = Question.objects.values_list('id')
            q = Question.objects.get(id=random.choice(q_ids)[0])

            Answer.objects.create(
                rating=f.random_int(min=-100, max=100),
                author=u,
                question=q,
                content=f.text(),
                date_added=timezone.now()
            )
        pass

    def fill_tags(self):
        for i in range(self.TAGS_COUNT):
            Tag.objects.create(
                title=f.word()[0:10],
                rating = 0,
            )
        pass

    def handle(self, *args, **options):
    #    if options['answers']:
    #        self.fill_answers(options.get('answers', 0))
    #    if options['authors']:
    #        self.fill_authors(options.get('authors', 0))
    #    if options['questions']:
    #       self.fill_questions(options.get('questions', 0))
    #    if options['tags']:
    #       self.fill_tags(options.get('tags', 0))
            self.fill_authors()
            self.fill_questions()
            self.fill_answers()
            self.fill_tags()
