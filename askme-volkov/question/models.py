from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist


class ProfileManager(models.Manager):
    def by_id(self, pid):
        try:
            profile = self.get(pk=pid)
        except ObjectDoesNotExist as e:
            print(e)
            return None
        return profile

    def update_rating(self, pid):
        profile = self.by_id(pid)
        if profile is None:
            print("Profile not fount")
            return

        rating = 0
        for q in Question.objects.by_profile_id(pid):
            rating += q.rating
        for a in Answer.objects.by_profile_id(pid):
            rating += a.rating

        profile.rating = rating
        profile.save()

    def update_ratings(self):
        for profile_id in self.values_list('pk', flat=True):
            self.update_rating(profile_id)

    def top(self, top_amount):
        sorted_profiles = self.order_by("-rating")
        top = sorted_profiles[:top_amount]
        return top

#class Author(models.Model):
#    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 #   avatar = models.ImageField(upload_to="avatars/")
 #   rating = models.IntegerField()

#    def __str__(self):
 #       return self.user.name

class Profile(AbstractUser):
    avatar = models.CharField(max_length=255)
    rating = models.IntegerField(default=0,
                                 null=False,
                                 blank=False)

    objects = ProfileManager()

    def __str__(self):
        return f"PK: {str(self.pk)}; Username: {self.username}"


class LikeManager(models.Manager):
    def by_question_id(self, qid):
        return self.filter(question__id=qid)

    def by_answer_id(self, aid):
        return self.filter(answer__id=aid)


class Like(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    LIKE = 1
    NEUTRAL = 0
    DISLIKE = -1
    RATING = [
        (LIKE, 'Like'),
        (NEUTRAL, 'Neutral'),
        (DISLIKE, 'Dislike'),
    ]
    rating = models.SmallIntegerField(choices=RATING,
                                      default=NEUTRAL,
                                      null=False,
                                      blank=False)

    objects = LikeManager()

    class Meta:
        unique_together = ('content_type', 'object_id', 'author')

    def __str__(self):
        return f"Like by {self.author.username}: {self.rating}"


class TagManager(models.Manager):
    def by_name(self, name):
        try:
            tag = self.get(name=name)
        except ObjectDoesNotExist as e:
            print(e)
            return None
        return tag

    def update_counter(self, tag_name):
        tag = self.by_name(tag_name)
        tag.counter = Question.objects.by_tag(tag_name).count()
        tag.save()

    def update_counters(self):
        for name in self.values_list("name", flat=True):
            self.update_counter(name)

    def top(self, top_amount):
        top = self.order_by('-counter')
        return top[:top_amount]


class Tag(models.Model):
    name = models.CharField(max_length=255,
                            unique=True,
                            null=False,
                            blank=False)
    counter = models.IntegerField(default=0,
                                  null=False,
                                  blank=False)

    objects = TagManager()

    def __str__(self):
        return f"PK: {self.pk}; Name: {self.name}"


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')

    def best(self):
        return self.order_by('-rating')

    def by_tag(self, tag_name):
        return self.filter(tags__name=tag_name)

    def by_question_id(self, qid):
        try:
            question = self.get(pk=qid)
        except ObjectDoesNotExist as e:
            print(e)
            return None
        return question

    def by_profile_id(self, pid):
        return self.filter(author_id=pid)

    def update_rating(self, qid):
        question = self.by_question_id(qid)
        if question is None:
            return

        rating = 0
        for like in Like.objects.by_question_id(qid):
            rating += like.rating
        question.rating = rating
        question.save()

    def update_ratings(self):
        for question_id in self.values_list('pk', flat=True):
            self.update_rating(question_id)


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,
                             null=False,
                             blank=False)
    content = models.CharField(max_length=1000,
                               null=False,
                               blank=False)
    tags = models.ManyToManyField(Tag)
    date = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like, related_query_name='question', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0,
                                 null=False,
                                 blank=False)

    objects = QuestionManager()

    def __str__(self):
        return f"QID({str(self.pk)}): " + self.content[:30]


class AnswerManager(models.Manager):
    def by_question_id(self, qid):
        return self.filter(question_id=qid)

    def by_profile_id(self, pid):
        return self.filter(author_id=pid)

    def by_answer_id(self, aid):
        try:
            answer = self.get(pk=aid)
        except ObjectDoesNotExist as e:
            print(e)
            return None
        return answer

    def update_rating(self, aid):
        answer = self.by_answer_id(aid)
        if answer is None:
            return

        rating = 0
        for like in Like.objects.by_answer_id(aid):
            rating += like.rating
        answer.rating = rating
        answer.save()

    def update_ratings(self):
        for answer_id in self.values_list('pk', flat=True):
            self.update_rating(answer_id)


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000,
                               null=False,
                               blank=False)
    likes = GenericRelation(Like, related_query_name='answer', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0,
                                 null=False,
                                 blank=False)

    objects = AnswerManager()

    def __str__(self):
        return f"PK:{str(self.pk)}; Content: {self.content[:30]}"
