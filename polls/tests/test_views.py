# CA3: Test and Security

"""
This file defines all the automated tests for the views in the internal app polls.
Each test is a function that interacts with a certain view and evaluates its response
against a pre-defined assertion. If the assertion is correct, the test has passed.
If the assertion is incorrect, the test has failed.
Each test tests only one functionality of the view, for this reason, tests are grouped
together into classes. Each class represents a suite of tests for a particular view.
"""

import random

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

import polls.views
from polls.models import Question, Choice


class IndexViewTest(TestCase):  # index view test suite
    number_of_questions = 10  # field to be available to all test cases

    @classmethod
    def setUpTestData(cls):  # prepares parameters that will be shared by the test cases
        # creates 10 mock questions
        for question_number in range(cls.number_of_questions):
            Question.objects.create(
                genre='Progressive Metal',
                year='1992',
                text='What is the best Progressive Metal album of 1992?'
            )

    def test_view_http_request_is_redirected_to_https(self):  # view should be accessed through HTTPS requests only
        response = self.client.get('/polls/')  # sends GET request to view
        self.assertEqual(response.status_code, 301)  # expects response status code to be 301 due to redirection

    def test_view_url_exists_at_desired_location(self):  # view should be accessible at its defined url
        response = self.client.get('/polls/', SERVER_NAME='localhost', secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_url_accessible_by_name(self):  # view should be internally accessible by its name tag
        response = self.client.get(reverse('polls:index'), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_uses_correct_template(self):  # view should render specific template
        response = self.client.get(reverse('polls:index'), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertTemplateUsed(response, 'polls/index.html')  # expects response to return adequate template

    def test_view_lists_all_questions_descending(self):  # view should return list of all questions in descending order
        response = self.client.get(reverse('polls:index'), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view

        # expects 'question_list' to be in the response's context
        self.assertTrue('question_list' in response.context)
        # expects 'question_list' to be the same as the number of questions created
        self.assertEqual(len(response.context['question_list']), self.number_of_questions)
        # expects 'question_list's elements to be ordered from newest to oldest
        self.assertEqual(list(response.context['question_list']),
                         sorted(response.context['question_list'], key=lambda x: x.pub_date, reverse=True))


class DetailViewTest(TestCase):  # detail view test suite
    question = Question  # question model to be available to all test cases
    choice = Choice  # choice model to be available to all test cases

    @classmethod
    def setUpClass(cls):  # prepares parameters that will be shared by the test cases
        super().setUpClass()
        # creates mock question and choice
        cls.question = Question.objects.create(genre='Progressive Metal', year='1992',
                                               text='What is the best Progressive Metal album of 1992?')
        cls.choice = Choice.objects.create(question=cls.question, title='Images And Words', artist='Dream Theater')

    def test_view_http_request_is_redirected_to_https(self):  # view should be accessed through HTTPS requests only
        response = self.client.get(f'/polls/{self.question.id}/', SERVER_NAME='localhost')  # sends GET request to view
        self.assertEqual(response.status_code, 301)  # expects response status code to be 301 due to redirection

    def test_view_url_exists_at_desired_location(self):  # view should be accessible at its defined url
        response = self.client.get(f'/polls/{self.question.id}/', SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_url_accessible_by_name(self):  # view should be internally accessible by its name tag
        response = self.client.get(reverse('polls:detail', args=[self.question.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_uses_correct_template(self):  # view should render specific template
        response = self.client.get(reverse('polls:detail', args=[self.question.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertTemplateUsed(response, 'polls/detail.html')  # expects response to return adequate template

    def test_view_vote_method(self):  # view should assign the vote to the correct object
        last_number_of_votes = self.choice.votes  # retrieves choice's current number of votes

        # negative test
        # sends POST request with choice id
        response = self.client.post(reverse('polls:vote', args=[self.question.id]), data={'choice': self.choice.id},
                                    SERVER_NAME='localhost', secure=True)
        self.choice.refresh_from_db()  # refreshes object's state to reflect database

        # expects redirection after voting
        self.assertEqual(response.status_code, 302)
        # expects number of votes to be the same since the user was NOT logged-in
        self.assertEqual(self.choice.votes, last_number_of_votes)

        user = User.objects.create_user(username='username')  # creates mock user
        self.client.force_login(user)  # logs-in in mock user ignoring credentials

        # positive test
        # sends POST request with choice id
        response = self.client.post(reverse('polls:vote', args=[self.question.id]), data={'choice': self.choice.id},
                                    SERVER_NAME='localhost', secure=True)
        self.choice.refresh_from_db()  # refreshes object's state to reflect database

        # expects redirection after voting
        self.assertEqual(response.status_code, 302)
        # expects number of votes to have increased since the user was logged-in
        self.assertGreater(self.choice.votes, last_number_of_votes)


class ResultsViewTest(TestCase):  # results view test suite
    question = Question  # question model to be available to all test cases

    @classmethod
    def setUpClass(cls):  # prepares parameters that will be shared by the test cases
        super().setUpClass()
        # creates mock question
        cls.question = Question.objects.create(genre='Progressive Metal', year='1992',
                                               text='What is the best Progressive Metal album of 1992?')

    def test_view_http_request_is_redirected_to_https(self):  # view should be accessed through HTTPS requests only
        response = self.client.get(f'/polls/{self.question.id}/results/',
                                   SERVER_NAME='localhost')  # sends GET request to view
        self.assertEqual(response.status_code, 301)  # expects response status code to be 301 due to redirection

    def test_view_url_exists_at_desired_location(self):  # view should be accessible at its defined url
        response = self.client.get(f'/polls/{self.question.id}/results/', SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_url_accessible_by_name(self):  # view should be internally accessible by its name tag
        response = self.client.get(reverse('polls:results', args=[self.question.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_uses_correct_template(self):  # view should render specific template
        response = self.client.get(reverse('polls:results', args=[self.question.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertTemplateUsed(response, 'polls/results.html')  # expects response to return adequate template


class CreateViewTest(TestCase):  # create view test suite
    user = User  # user model to be available to all test cases

    @classmethod
    def setUpTestData(cls):  # prepares parameters that will be shared by the test cases
        super().setUpTestData()
        cls.user = User.objects.create_user(username='username')  # creates mock user

    def test_view_http_request_is_redirected_to_https(self):  # view should be accessed through HTTPS requests only
        response = self.client.get(f'/polls/create', SERVER_NAME='localhost')  # sends GET request to view
        self.assertEqual(response.status_code, 301)  # expects response status code to be 301 due to redirection

    def test_view_returns_302_if_user_not_logged_in(self):  # view should be restricted to logged-in users
        response = self.client.get(f'/polls/create', SERVER_NAME='localhost', secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 302)  # expects response status code to be 302 due to redirection

    def test_view_url_exists_at_desired_location(self):  # view should be accessible at its defined url
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials
        response = self.client.get(f'/polls/create', SERVER_NAME='localhost', secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_url_accessible_by_name(self):  # view should be internally accessible by its name tag
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials
        response = self.client.get(reverse('polls:create'), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_uses_correct_template(self):  # view should render specific template
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials
        response = self.client.get(reverse('polls:create'), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertTemplateUsed(response, 'polls/create.html')  # expects response to return adequate template

    def test_view_offers_correct_form_fields(self):  # view should offer the user the correct form fields
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials
        response = self.client.get(reverse('polls:create'), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view

        # expects response's context to contain keys 'genres' and 'years'
        self.assertTrue(all(keys in response.context.keys() for keys in ('genres', 'years')))
        # expects the values associated with those keys to be the same as the ones from 'get_parameters()'
        self.assertEqual((response.context['genres'], response.context['years']), polls.views.get_parameters())

    def test_view_post_creates_correct_objects(self):  # view should attempt to create poll with correct parameters
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials
        last_question = Question.objects.last()  # retrieves most recent question before posting
        last_number_of_choices = Choice.objects.count()  # retrieves amount of choices before posting
        # get lists of all available genres and years to choose from and randomly select one of each
        genre, year = [random.choice(params) for params in polls.views.get_parameters()]

        # send POST request with selected genre and year
        response = self.client.post(reverse('polls:create_selected'), data={'genre': genre, 'year': year},
                                    SERVER_NAME='localhost', secure=True)
        new_question = Question.objects.last()  # retrieves most recent question after posting
        new_number_of_choices = Choice.objects.count()  # retrieves amount of choices after posting

        if response.status_code == 302:  # expects 302 redirection after successful creation
            self.assertNotEqual(new_question, last_question)  # expects there to be a new question
            self.assertEqual(new_question.text, f'What is the best {genre} album of {year}?')  # expects a standard text
            self.assertGreater(new_number_of_choices, last_number_of_choices)  # expects there to be more choices
        else:  # if creation fails
            self.assertEqual(new_question, last_question)  # expects there NOT to be a new question
            self.assertEqual(new_number_of_choices, last_number_of_choices)  # expects there NOT to be more choices
