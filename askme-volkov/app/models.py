from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class QuestionManager(models.Manager):
    def hot(self):
        return self.order_by('-rating')
    def newest(self):
        return self.order_by('-date_added')

class AuthorManager(models.Manager):
    def best_members(self):
        return self.order_by('-rating')

class TagManager(models.Manager):
    def best_tags(self):
        return self.order_by('-rating')


class Author (models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    avatar = models.ImageField(upload_to = 'avatars/', default = 'None/no-img.png')
    rating = models.IntegerField()
    def __str__(self):
        return self.user.username
    objects = AuthorManager()

class Tag (models.Model):
    title = models.CharField(max_length=128)
    rating = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    objects = TagManager()


class Answer(models.Model):
    content = models.TextField()
    rating = models.IntegerField()

    author = models.ForeignKey(
        'Author', on_delete = models.CASCADE
    )
    date_added = models.DateTimeField()
    is_correct = models.BooleanField(default=0)
    def __str__(self):
                return self.content

class Question(models.Model):
    title = models.TextField(max_length=128)
    content = models.TextField()
    rating = models.IntegerField()
    author = models.ForeignKey(
        'Author', on_delete = models.CASCADE
    )
    answers = models.ManyToManyField(Answer, verbose_name="list of answers")
    tags = models.ManyToManyField(Tag, verbose_name="list of tags")
    date_added = models.DateTimeField()
    objects = QuestionManager()

    def __str__(self):
            return self.title