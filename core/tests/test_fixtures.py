# from django.core import management
# from django.test import TestCase

# from categories.models import Category
# from core.models import Configuration
# from glossary.models import GlossaryItem
# from questions.models import Question
# from quizs.models import Quiz, QuizRelationship
# from tags.models import Tag


# # TODO: doesn't work anymore after the repo split
# class FixturesTest(TestCase):
#     # fixtures = [
#     #     "data/categories.yaml",
#     #     "data/tags.yaml",
#     #     "data/questions.yaml",
#     #     "data/quiz.yaml",
#     #     "data/quiz-relationships.yaml",
#     #     "data/ressources-glossaire.yaml",
#     # ]

#     # def test_fixtures_load_successfully(self):
#     #     self.assertTrue(Category.objects.count())
#     #     self.assertTrue(Tag.objects.count())
#     #     self.assertTrue(Question.objects.count())
#     #     self.assertTrue(Quiz.objects.count())
#     #     self.assertTrue(QuizRelationship.objects.count())
#     #     self.assertTrue(GlossaryItem.objects.count())

#     # def test_flat_fixtures_load_successfully(self):
#     #     management.call_command("init_db")
#     #     self.assertTrue(Configuration.objects.count())
#     #     self.assertTrue(Category.objects.count())
#     #     self.assertTrue(Tag.objects.count())
#     #     self.assertTrue(Question.objects.count())
#     #     self.assertTrue(Quiz.objects.count())
#     #     self.assertTrue(QuizRelationship.objects.count())
#     #     self.assertTrue(GlossaryItem.objects.count())
