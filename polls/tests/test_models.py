# CA3: Test and Security

"""
This file defines all the tests for the models of the internal app polls.
Each test is a function that interacts with a certain model and evaluates its parameters
against a pre-defined assertion. If the assertion is correct, the test has passed.
If the assertion is incorrect, the test has failed.
Each test tests only one parameter of the model, for this reason, tests are grouped
together into classes. Each class represents a suite of tests for a particular model.
"""

import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question, Choice


class QuestionModelTest(TestCase):  # question model test suite
    question = Question  # question model to be used in all test cases

    @classmethod
    def setUpTestData(cls):  # prepares parameters that will be shared by the test cases
        # creates mock question
        cls.question = Question.objects.create(genre='Progressive Metal', year='1992',
                                               text='What is the best Progressive Metal album of 1992?')

    def test_genre_label(self):  # field should have the specified label
        field_label = self.question._meta.get_field('genre').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'genre')  # expects label to be as specified in models

    def test_year_label(self):  # field should have the specified label
        field_label = self.question._meta.get_field('year').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'year')  # expects label to be as specified in models

    def test_text_label(self):  # field should have the specified label
        field_label = self.question._meta.get_field('text').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'text')  # expects label to be as specified in models

    def test_pub_date_label(self):  # field should have the specified label
        field_label = self.question._meta.get_field('pub_date').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'date published')  # expects label to be as specified in models

    def test_genre_max_length(self):  # text field should have specified maximum length
        max_length = self.question._meta.get_field('genre').max_length  # gets field maximum length from model
        self.assertEqual(max_length, 50)  # expects maximum length to be as specified in models

    def test_text_max_length(self):  # text field should have specified maximum length
        max_length = self.question._meta.get_field('text').max_length  # gets field maximum length from model
        self.assertEqual(max_length, 100)  # expects maximum length to be as specified in models

    def test_object_name_is_field_text(self):  # stringified object should be same as field text
        expected_object_name = self.question.text  # gets field text from model
        self.assertEqual(str(self.question), expected_object_name)  # expects text to be same as stringified object

    def test_was_published_recently(self):  # field should be true if question was published in the last 24 hours
        now = timezone.now()  # gets current time
        # expects field to be same as whether the publication time is between 24 hours ago and now
        self.assertEqual(self.question.was_published_recently(),
                         now - datetime.timedelta(days=1) <= self.question.pub_date <= now)


class ChoiceModelTest(TestCase):  # choice model test suite
    question = Question  # question model to be used in all test cases
    choice = Choice  # choice model to be used in all test cases

    @classmethod
    def setUpTestData(cls):  # prepares parameters that will be shared by the test cases
        # creates mock question and choice
        cls.question = Question.objects.create(genre='Progressive Metal', year='1992',
                                               text='What is the best Progressive Metal album of 1992?')
        cls.choice = Choice.objects.create(question=cls.question, title='Images And Words', artist='Dream Theater')

    def test_question_label(self):  # field should have the specified label
        field_label = self.choice._meta.get_field('question').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'question')  # expects label to be as specified in models

    def test_image_label(self):  # field should have the specified label
        field_label = self.choice._meta.get_field('image').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'image')  # expects label to be as specified in models

    def test_title_label(self):  # field should have the specified label
        field_label = self.choice._meta.get_field('title').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'title')  # expects label to be as specified in models

    def test_artist_label(self):  # field should have the specified label
        field_label = self.choice._meta.get_field('artist').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'artist')  # expects label to be as specified in models

    def test_year_label(self):  # field should have the specified label
        field_label = self.choice._meta.get_field('year').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'year')  # expects label to be as specified in models

    def test_genres_label(self):  # field should have the specified label
        field_label = self.choice._meta.get_field('genres').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'genres')  # expects label to be as specified in models

    def test_votes_label(self):  # field should have the specified label
        field_label = self.choice._meta.get_field('votes').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'votes')  # expects label to be as specified in models

    def test_country_label(self):  # field should have the specified label
        field_label = self.choice._meta.get_field('country').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'country')  # expects label to be as specified in models

    def test_url_label(self):  # field should have the specified label
        field_label = self.choice._meta.get_field('url').verbose_name  # gets field label from model
        self.assertEqual(field_label, 'url')  # expects label to be as specified in models

    def test_image_max_length(self):  # text field should have specified maximum length
        max_length = self.choice._meta.get_field('image').max_length  # gets field maximum length from model
        self.assertEqual(max_length, 1000)  # expects maximum length to be as specified in models

    def test_title_max_length(self):  # text field should have specified maximum length
        max_length = self.choice._meta.get_field('title').max_length  # gets field maximum length from model
        self.assertEqual(max_length, 100)  # expects maximum length to be as specified in models

    def test_artist_max_length(self):  # text field should have specified maximum length
        max_length = self.choice._meta.get_field('artist').max_length  # gets field maximum length from model
        self.assertEqual(max_length, 100)  # expects maximum length to be as specified in models

    def test_genres_max_length(self):  # text field should have specified maximum length
        max_length = self.choice._meta.get_field('genres').max_length  # gets field maximum length from model
        self.assertEqual(max_length, 500)  # expects maximum length to be as specified in models

    def test_country_max_length(self):  # text field should have specified maximum length
        max_length = self.choice._meta.get_field('country').max_length  # gets field maximum length from model
        self.assertEqual(max_length, 50)  # expects maximum length to be as specified in models

    def test_url_max_length(self):  # text field should have specified maximum length
        max_length = self.choice._meta.get_field('url').max_length  # gets field maximum length from model
        self.assertEqual(max_length, 500)  # expects maximum length to be as specified in models

    def test_object_name_is_artist_hyphen_title(self):  # stringified object should follow specified standard
        expected_object_name = f'{self.choice.artist} - {self.choice.title}'  # gets standard from model
        self.assertEqual(str(self.choice), expected_object_name)  # expects stringified object to be same as standard
