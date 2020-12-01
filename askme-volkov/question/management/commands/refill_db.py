from django.core.management.base import BaseCommand, CommandError
from question.models import Profile, Tag, Question, Answer, Like
from faker import Faker
import time

faker = Faker()

generated_tags = [
    "Doom",
    "Test",
    "Newyear",
    "Birthday",
    "Election",
    "Russia",
    "Trump", ]

generated_names = [
    "Nikita",
    "Misha",
    "Nastya",
    "NeKostya"]


class Command(BaseCommand):
    help = 'Empty and fill database with fake data'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        def positive_int(value):
            value = int(value)
            if value < 0:
                raise CommandError("Argument must be positive integer")
            return value

        parser.add_argument('--profiles', type=positive_int)
        parser.add_argument('--max_questions_per_profile', type=positive_int)
        parser.add_argument('--max_answers_per_question', type=positive_int)
        parser.add_argument('--max_likes', type=positive_int)
        parser.add_argument('--max_dislikes', type=positive_int)

        parser.add_argument('-s', '--db_size', type=str, help='Preset amounts')

    def add_tags(self):
        for tag_name in generated_tags:
            Tag.objects.create(name=tag_name)

    def add_profiles(self, amount):
        for name in generated_names:
            Profile.objects.create(username=name, password="test")
        for i in range(amount - 4):
            Profile.objects.create(username=faker.user_name() + str(i), password="test")

    def add_likes(self, post, profiles, max_likes, max_dislikes):
        max_likes = faker.random.randint(0, max_likes)
        max_dislikes = faker.random.randint(0, max_dislikes)

        if post.author.username in generated_names:
            max_dislikes = 0

        likers = faker.random.sample(profiles, max_likes + max_dislikes)
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

            like = Like(content_object=post, author=liker, rating=rating)
            likes.append(like)
        Like.objects.bulk_create(likes)

    def add_questions(self, max_questions_per_profile, max_likes, max_dislikes):
        all_profiles = list(Profile.objects.all())
        all_tags = list(Tag.objects.all())
        questions = []

        for profile in all_profiles:
            for _ in range(faker.random.randint(0, max_questions_per_profile)):
                title = faker.sentence(5)
                content = faker.sentence(20)

                q = Question.objects.create(author=profile,
                                            title=title,
                                            content=content)
        Question.objects.bulk_create(questions)

        questions = list(Question.objects.all())
        for question in questions:
            tags = faker.random.sample(all_tags, faker.random.randint(1, len(all_tags)))
            question.tags.set(tags)
            self.add_likes(question, all_profiles, max_likes, max_dislikes)

        Question.objects.update_ratings()
        Tag.objects.update_counters()

    def add_answers(self, max_answers_per_question, max_likes, max_dislikes):
        all_profiles = list(Profile.objects.all())
        all_questions = list(Question.objects.all())

        answers = []
        for q in all_questions:
            for i in range(faker.random.randint(0, max_answers_per_question)):
                author = faker.random.choice(all_profiles)
                content = faker.sentence(30)
                a = Answer(author=author,
                           question=q,
                           content=content)
                answers.append(a)
        Answer.objects.bulk_create(answers)

        answers = list(Answer.objects.all())
        for answer in answers:
            self.add_likes(answer, all_profiles, max_likes, max_dislikes)

        Answer.objects.update_ratings()

    def handle(self, *args, **options):
        Profile.objects.all().delete()
        Tag.objects.all().delete()
        assert (Profile.objects.count() == 0)
        assert (Tag.objects.count() == 0)
        assert (Like.objects.count() == 0)
        assert (Question.objects.count() == 0)
        assert (Answer.objects.count() == 0)

        db_size = options['db_size']

        profiles = options.get('profiles') or 25
        max_questions_per_profile = options.get('max_questions_per_profile') or 5
        max_answers_per_question = options.get('max_answers_per_question') or 5


        if db_size:
            if db_size == 'small':
                profiles = 20
                max_questions_per_profile = 30
                max_answers_per_question = 60
            elif db_size == 'medium':
                profiles = 1000
                max_questions_per_profile = 5000
                max_answers_per_question = 10000
            elif db_size == 'large':
                profiles =  10000
                max_questions_per_profile = 100000
                max_answers_per_question = 1000000


        max_likes = options.get('max_likes') or int(profiles / 2)
        max_dislikes = options.get('max_dislikes') or int(profiles / 2)

        if max_likes + max_dislikes > profiles:
            raise BaseCommand("Summary amount of likes and dislikes is less than profiles amount")

        start = time.time()
        self.add_profiles(profiles)
        print(f"Added profiles: {time.time() - start}")

        self.add_tags()
        print(f"Added tags: {time.time() - start}")

        self.add_questions(max_questions_per_profile, max_likes, max_dislikes)
        print(f"Added questions: {time.time() - start}")

        self.add_answers(max_answers_per_question, max_likes, max_dislikes)
        print(f"Added answers: {time.time() - start}")

        Profile.objects.update_ratings()
        print(f"Updated profile ratings")

        print("Database filled")
