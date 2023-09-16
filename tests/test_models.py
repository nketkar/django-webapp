from django.contrib.auth import get_user_model
from django.test import TestCase

from main.models import Answer, Question
from .factories import create_questions


def create_user():
    User = get_user_model()
    user = User.objects.create(username='joker')
    return user


class AnswerTestCase(TestCase):

    def test_save(self):
        create_questions()
        que = Question.objects.first()
        Answer.objects.create(question=que, answer='Cat', user=create_user())

        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(Answer.objects.first().answer, 'Cat')
