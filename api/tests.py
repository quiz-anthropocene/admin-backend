from django.test import TestCase
from django.urls import reverse
from api import models
import io
from rest_framework.parsers import JSONParser


class myTestCase(TestCase):
    def setUp(self):
        tag0 = models.Tag.objects.create(name="Tag 0")
        tag1 = models.Tag.objects.create(name="Tag 1")
        category0 = models.Category.objects.create(name="Cat 0")
        models.Question.objects.create(publish=False, author="author0")
        question1 = models.Question.objects.create(publish=True, author="author1")
        question1.tags.add(tag0)
        question1.tags.add(tag1)
        question1.category = category0
        question1.save()
        question2 = models.Question.objects.create(publish=True, author="author2")
        question2.tags.add(tag1)
        question2.save()

    def test_main(self):
        response = self.client.get(reverse('api:index'))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf8')
        self.assertIn('Welcome', html)

    def test_question_list(self):
        response = self.client.get(reverse('api:question_list'))
        self.assertEqual(response.status_code, 200)
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 2)

        response = self.client.get(reverse('api:question_list'), {"author": "author1"})
        self.assertEqual(response.status_code, 200)
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 1)

        response = self.client.get(reverse('api:question_list'), {"tag": "Tag 0"})
        self.assertEqual(response.status_code, 200)
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 1)

        response = self.client.get(reverse('api:question_list'), {"tag": "Tag 1"})
        self.assertEqual(response.status_code, 200)
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 2)

        response = self.client.get(reverse('api:question_list'), {"category": "Cat 0"})
        self.assertEqual(response.status_code, 200)
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 1)
