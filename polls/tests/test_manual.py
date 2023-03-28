# CA3: Test and Security

"""
This file defines all the manual tests for the internal app polls.
Each test is a function that interacts with a certain view and evaluates its response
against a pre-defined assertion. If the assertion is correct, the test has passed.
If the assertion is incorrect, the test has failed.
Each test tests only one functionality of the view, for this reason, tests are grouped
together into classes. Each class represents a suite of tests for a particular view.

Because the tests defined here are manual, user input is expected. This means that
execution stops and waits for the tester to input some data. The tags defined here
should be used to exclude these tests when automating.
"""

from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse

import polls.views
from polls.models import Question, Choice


@tag('manual')  # tag can be used to include/exclude test from the command line
class DetailViewTest(TestCase):  # detail view test suite
    user = User  # user model to be used in all test cases
    question = Question  # question model to be used in all test cases
    choice_1 = Choice  # 1st choice model to be used in all test cases
    choice_2 = Choice  # 2nd choice model to be used in all test cases

    @classmethod
    def setUpTestData(cls):  # prepares parameters that will be shared by the test cases
        super().setUpTestData()
        # creates mock objects: user, question, choices 1 and 2
        cls.user = User.objects.create_user(username='username')
        cls.question = Question.objects.create(genre='Progressive Metal', year='1992',
                                               text='What is the best Progressive Metal album of 1992?')
        cls.choice_1 = Choice.objects.create(question=cls.question, title='Images And Words', artist='Dream Theater')
        cls.choice_2 = Choice.objects.create(question=cls.question, title='Into The Everflow', artist='Psychotic Waltz')

    def test_view_vote_method(self):  # view should assign the vote to the correct object
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials
        choices = Choice.objects.filter(question_id=self.question.id)  # retrieves all choices associated with question

        # CLI interaction block
        print("\nVOTE IN A POLL")

        # displays list of choices and read input
        opt = "-1"
        while not opt.isnumeric() or int(opt) - 1 not in range(len(choices)):
            print(f"\n{str(self.question)}")
            print("Choices:")
            for i, c in enumerate(choices, start=1):
                print('{0}. {1} {2}'.format(i, str(c), f'votes: {c.votes}'))
            opt = input("\nChoice #: ")
        choice = choices[int(opt) - 1]

        # number of votes choice had before posting
        last_number_of_votes = choice.votes

        # send POST request with chosen choice id
        response = self.client.post(reverse('polls:vote', args=[self.question.id]), data={'choice': choice.id},
                                    SERVER_NAME='localhost', secure=True)
        choice.refresh_from_db()  # refreshes choice so that it reflects database after posting

        self.assertEqual(response.status_code, 302)  # expects 302 redirection after voting
        self.assertGreater(choice.votes, last_number_of_votes)  # expect choice to have more votes

        # displays updated list of choices
        print(f"\n{str(self.question)}")
        print("Results:")
        for i, c in enumerate(choices, start=1):
            print('{0}. {1} {2}'.format(i, str(c), f'votes: {c.votes}'))


@tag('manual')  # tag can be used to include/exclude test from the command line
class CreateViewTest(TestCase):  # create view test suite
    user = User  # user model to be used in all test cases

    @classmethod
    def setUpTestData(cls):  # prepares parameters that will be shared by the test cases
        super().setUpTestData()
        cls.user = User.objects.create_user(username='username')  # creates mock user

    def test_view_post_creates_correct_objects(self):  # view should attempt to create poll with correct parameters
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials
        last_question = Question.objects.last()  # retrieves most recent question before posting
        last_number_of_choices = Choice.objects.count()  # retrieves amount of choices before posting
        genres, years = polls.views.get_parameters()  # get lists of all available genres and years to choose from

        # CLI interaction block
        print("\nCREATE A NEW POLL")

        # displays list of genres and read input
        opt = "-1"
        while not opt.isnumeric() or int(opt) - 1 not in range(len(genres)):
            print("\nGenres:")
            for i in range(0, len(genres), 2):
                if i + 1 == len(genres):
                    print('{0}. {1}'.format(i + 1, genres[i]))
                    break
                print('{0}. {1:25} {2}. {3}'.format(i + 1, genres[i], i + 2, genres[i + 1]))
            opt = input("\nGenre #: ")
        genre = genres[int(opt) - 1]

        # read input for year
        opt = "-1"
        while not opt.isnumeric() or int(opt) not in years:
            opt = input(f"Year ({years[-1]}-{years[0]}): ")
        year = int(opt)

        # send POST request with chosen genre and year
        response = self.client.post(reverse('polls:create_selected'), data={'genre': genre, 'year': year},
                                    SERVER_NAME='localhost', secure=True)
        new_question = Question.objects.last()  # retrieves most recent question after posting
        new_number_of_choices = Choice.objects.count()  # retrieves amount of choices after posting

        if response.status_code == 302:  # expects 302 redirection after successful creation
            self.assertNotEqual(new_question, last_question)  # expects there to be a new question
            self.assertEqual(new_question.text, f'What is the best {genre} album of {year}?')  # expects a standard text
            self.assertGreater(new_number_of_choices, last_number_of_choices)  # expects there to be more choices

            # displays newly created poll with its choices
            print("\nQuestion:")
            print(str(new_question))
            print("\nChoices:")
            for choice in Choice.objects.filter(question_id=new_question.id):
                print(str(choice))
        else:  # if creation fails
            self.assertEqual(new_question, last_question)  # expects there NOT to be a new question
            self.assertEqual(new_number_of_choices, last_number_of_choices)  # expects there NOT to be more choices

            # displays error message
            print("\nNo matches found!\n")
