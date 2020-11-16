from django.core.management.base import BaseCommand, CommandError
from question.models import Profile, Tag, Question, Answer, Like
from faker import Faker
import time

faker = Faker()

spooky_tags = [
    "Halloween",
    "Pumpkin",
    "Spooks",
    "Very spo0ky spooks",
    "Funny Spooks",
    "Spooky Spooks",
    "2sPo0kY4u is a scammer!!1", ]

spooky_names = [
    "2sPo0kY4u",
    "SpookyScarySkeleton",
    "xXxSPOOKSTERxXx",
    "Potato"]


class Command(BaseCommand):
    help = 'Empty and fill database with fake data'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('--profiles', type=int)
        parser.add_argument('--max_questions_per_profile', type=int)
        parser.add_argument('--max_answers_per_question', type=int)
        parser.add_argument('--max_likes', type=int)
        parser.add_argument('--max_dislikes', type=int)

    def add_tags(self):
        for tag_name in spooky_tags:
            Tag.objects.create(name=tag_name)

    def add_profiles(self, amount):
        for name in spooky_names:
            Profile.objects.create(username=name, password="spook")
        for i in range(amount - 4):
            Profile.objects.create(username=faker.user_name(), password="spook")

    def set_likes(self, post, profiles, max_likes, max_dislikes):
        max_likes = faker.random.randint(0, max_likes)
        max_dislikes = faker.random.randint(0, max_dislikes)

        if post.author.username in spooky_names:
            max_dislikes = 0

        # start = time.time()
        # print("Creating sample")
        likers = faker.random.sample(profiles, max_likes + max_dislikes)
        # print(f"Created sample: {time.time() - start}")
        curr_likes = 0
        curr_dislikes = 0
        likes = []
        for liker in likers:
            choices = []
            if curr_likes < max_likes:
                choices.append(Like.LIKE)
            if curr_dislikes < max_dislikes:
                choices.append(Like.DISLIKE)

            rating = faker.random.choice(choices)
            if rating == Like.LIKE:
                curr_likes += 1
            else:
                curr_dislikes += 1

            like = Like.objects.create(content_object=post, author=liker, rating=rating)
            # print(f"Created like: {time.time() - start}")
            likes.append(like)
        post.likes.set(likes)
        # print(f"Added likes: {time.time() - start}")

    def add_questions(self, max_questions_per_profile, max_likes, max_dislikes):
        all_profiles = list(Profile.objects.all())
        all_tags = list(Tag.objects.all())

        for profile in all_profiles:
            for _ in range(faker.random.randint(0, max_questions_per_profile)):
                # start = time.time()
                # print("Started adding question")
                title = faker.sentence(5)
                content = faker.sentence(20)

                tags = faker.random.sample(all_tags, faker.random.randint(1, len(all_tags)))
                # print(f"Created sample: {time.time() - start}")
                q = Question.objects.create(author=profile,
                                            title=title,
                                            content=content)
                # print(f"Created question: {time.time() - start}")
                q.tags.set(tags)
                # print(f"Added tags {time.time() - start}")
                self.set_likes(q, all_profiles, max_likes, max_dislikes)
                # print(f"Added likes: {time.time() - start}")
                q.save()
                # print(f"Saved question: {time.time() - start}")
                Question.objects.update_rating(q.id)
                # print(f"Updated question rating: {time.time() - start}")
                # print(f"Added question {_}")

    def add_answers(self, max_answers_per_question, max_likes, max_dislikes):
        all_profiles = list(Profile.objects.all())

        for q in Question.objects.all():
            for i in range(faker.random.randint(0, max_answers_per_question)):
                author = faker.random.choice(all_profiles)
                content = faker.sentence(30)
                a = Answer.objects.create(author=author,
                                          question=q,
                                          content=content)
                self.set_likes(a, all_profiles, max_likes, max_dislikes)
                a.save()
                Answer.objects.update_rating(a.id)

    def handle(self, *args, **options):
        Profile.objects.all().delete()
        Tag.objects.all().delete()

        profiles = options.get('profiles') or 25
        max_questions_per_profile = options.get('max_questions_per_profile') or 5
        max_answers_per_question = options.get('max_answers_per_question') or 5
        max_likes = options.get('max_likes') or int(profiles / 2)
        max_dislikes = options.get('max_dislikes') or int(profiles / 2)

        self.add_profiles(profiles)
        print("Added profiles")
        self.add_tags()
        print("Added tags")
        self.add_questions(max_questions_per_profile, max_likes, max_dislikes)
        print("Added questions")
        self.add_answers(max_answers_per_question, max_likes, max_dislikes)
        print("Added answers")

        print("Database filled")
