# CA3: Test and Security

"""
This file defines all the tests for the views in the internal app accounts.
Each test is a function that interacts with a certain view and evaluates its response
against a pre-defined assertion. If the assertion is correct, the test has passed.
If the assertion is incorrect, the test has failed.
Each test tests only one functionality of the view, for this reason, tests are grouped
together into classes. Each class represents a suite of tests for a particular view.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class SignUpViewTest(TestCase):  # sign up view test suite
    def test_view_http_request_is_redirected_to_https(self):  # view should be accessed through HTTPS requests only
        response = self.client.get('/accounts/signup/', SERVER_NAME='localhost')  # sends GET request to view
        self.assertEqual(response.status_code, 301)  # expects response status code to be 301 due to redirection

    def test_view_url_exists_at_desired_location(self):  # view should be accessible at its defined url
        response = self.client.get('/accounts/signup/', SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_url_accessible_by_name(self):  # view should be internally accessible by its name tag
        response = self.client.get(reverse('accounts:signup'), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_uses_correct_template(self):  # view should render specific template
        response = self.client.get(reverse('accounts:signup'), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertTemplateUsed(response, 'registration/signup.html')  # expects response to return adequate template

    def test_view_post_creates_correct_object(self):  # view should create objects with attributes input
        # creates mock new user attributes
        username = 'new_username'
        email = 'new_email@email.com'
        password = 'new_password'

        # sends POST request to view with new user attributes
        response = self.client.post(reverse('accounts:signup'),
                                    data={'username': username, 'email': email, 'password1': password},
                                    SERVER_NAME='localhost',
                                    secure=True)

        # retrieves newly created user from database
        user = User.objects.get(username=username)
        # expects new user to be in queryset containing all users
        self.assertIn(user, User.objects.all())
        # expects to be redirected to login page after successfully signing-up
        self.assertRedirects(response, reverse('login'), target_status_code=301)


class DetailViewTest(TestCase):  # detail view test suite
    user = User  # user model to be used in all test cases

    @classmethod
    def setUpClass(cls):  # prepares parameters that will be shared by the test cases
        super().setUpClass()
        cls.user = User.objects.create_user(username='username')  # creates mock user

    def test_view_http_request_is_redirected_to_https(self):  # view should be accessed through HTTPS requests only
        response = self.client.get(f'/accounts/{self.user.id}/detail/',
                                   SERVER_NAME='localhost')  # sends GET request to view
        self.assertEqual(response.status_code, 301)  # expects response status code to be 301 due to redirection

    def test_view_returns_302_if_user_not_logged_in(self):  # view should be restricted to logged-in users
        response = self.client.get(f'/accounts/{self.user.id}/detail/', SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 302)  # expects response status code to be 302 due to redirection

    def test_view_url_exists_at_desired_location(self):  # view should be accessible at its defined url
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        response = self.client.get(f'/accounts/{self.user.id}/detail/', SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_url_accessible_by_name(self):  # view should be internally accessible by its name tag
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        response = self.client.get(reverse('accounts:detail', args=[self.user.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_uses_correct_template(self):  # view should render specific template
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        response = self.client.get(reverse('accounts:detail', args=[self.user.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertTemplateUsed(response, 'accounts/detail.html')  # expects response to return adequate template

    def test_view_test_func_method(self):  # view should verify that requesting user owns the resource
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        # negative test
        response = self.client.get(reverse('accounts:detail', args=[self.user.id - 1]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view with wrong user id
        self.assertEqual(response.status_code, 403)  # expects response status code to be 403 forbidden

        # positive test
        response = self.client.get(reverse('accounts:detail', args=[self.user.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view with right user id
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success


class DeleteViewTest(TestCase):  # delete view test suite
    user = User  # user model to be used in all test cases

    @classmethod
    def setUpClass(cls):  # prepares parameters that will be shared by the test cases
        super().setUpClass()
        cls.user = User.objects.create_user(username='username', password='password')  # creates mock user

    def test_view_http_request_is_redirected_to_https(self):  # view should be accessed through HTTPS requests only
        response = self.client.get(f'/accounts/{self.user.id}/delete/',
                                   SERVER_NAME='localhost')  # sends GET request to view
        self.assertEqual(response.status_code, 301)  # expects response status code to be 301 due to redirection

    def test_view_returns_302_if_user_not_logged_in(self):  # view should be restricted to logged-in users
        response = self.client.get(f'/accounts/{self.user.id}/delete/', SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 302)  # expects response status code to be 302 due to redirection

    def test_view_url_exists_at_desired_location(self):  # view should be accessible at its defined url
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        response = self.client.get(f'/accounts/{self.user.id}/delete/', SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_url_accessible_by_name(self):  # view should be internally accessible by its name tag
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        response = self.client.get(reverse('accounts:delete', args=[self.user.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_uses_correct_template(self):  # view should render specific template
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        response = self.client.get(reverse('accounts:delete', args=[self.user.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertTemplateUsed(response, 'accounts/delete.html')  # expects response to return adequate template

    def test_view_post_deletes_correct_object(self):  # view should delete only the indicated object
        self.client.login(username='username', password='password')  # logs-in in mock user using credentials

        # negative test
        # sends POST request to view with user attributes with wrong password
        response = self.client.post(reverse('accounts:delete', args=[self.user.id]),
                                    data={'pk': self.user.id, 'password': 'wrong_password'}, SERVER_NAME='localhost',
                                    secure=True)
        self.assertEqual(response.context['fail'], 1)  # expects response to return fail flag
        self.assertIn(self.user, User.objects.all())  # expects user to NOT have been removed from the database

        # positive test
        # sends POST request to view with user attributes with right password
        response = self.client.post(reverse('accounts:delete', args=[self.user.id]),
                                    data={'pk': self.user.id, 'password': 'password'}, SERVER_NAME='localhost',
                                    secure=True)
        self.assertTrue('fail' not in response.context.keys())  # expects response to NOT return fail flag
        self.assertNotIn(self.user, User.objects.all())  # expects user to have been removed from the database

    def test_view_test_func_method(self):  # view should verify that requesting user owns the resource
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        # negative test
        response = self.client.get(reverse('accounts:delete', args=[self.user.id - 1]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view with wrong user id
        self.assertEqual(response.status_code, 403)  # expects response status code to be 403 forbidden

        # positive test
        response = self.client.get(reverse('accounts:delete', args=[self.user.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view with right user id
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success


class UpdateEmailViewTest(TestCase):  # update email view test suite
    user = User  # user model to be used in all test cases

    @classmethod
    def setUpClass(cls):  # prepares parameters that will be shared by the test cases
        super().setUpClass()
        cls.user = User.objects.create_user(username='username')  # create mock user

    def test_view_http_request_is_redirected_to_https(self):  # view should be accessed through HTTPS requests only
        response = self.client.get(f'/accounts/{self.user.id}/detail/email',
                                   SERVER_NAME='localhost')  # sends GET request to view
        self.assertEqual(response.status_code, 301)  # expects response status code to be 301 due to redirection

    def test_view_returns_302_if_user_not_logged_in(self):  # view should be restricted to logged-in users
        response = self.client.get(f'/accounts/{self.user.id}/detail/email', SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 302)  # expects response status code to be 302 due to redirection

    def test_view_url_exists_at_desired_location(self):  # view should be accessible at its defined url
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        response = self.client.get(f'/accounts/{self.user.id}/detail/email', SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_url_accessible_by_name(self):  # view should be internally accessible by its name tag
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        response = self.client.get(reverse('accounts:update_email', args=[self.user.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success

    def test_view_uses_correct_template(self):  # view should render specific template
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        response = self.client.get(reverse('accounts:update_email', args=[self.user.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view
        self.assertTemplateUsed(response, 'accounts/change_email.html')  # expects response to return adequate template

    def test_view_post_updates_correct_object(self):  # view should update only the indicated object
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials
        new_email = 'new_email@email.com'  # new email to be updated to database

        # sends POST request with user id and new email to be updated to database
        self.client.post(reverse('accounts:update_email', args=[self.user.id]),
                         data={'pk': self.user.id, 'email': new_email}, SERVER_NAME='localhost',
                         secure=True)
        self.user.refresh_from_db()  # refreshes mock user to reflect update
        self.assertEqual(self.user.email, new_email)  # expects user email to the same as new email

    def test_view_test_func_method(self):  # view should verify that requesting user owns the resource
        self.client.force_login(self.user)  # logs-in in mock user ignoring credentials

        # negative test
        response = self.client.get(reverse('accounts:update_email', args=[self.user.id - 1]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view with wrong user id
        self.assertEqual(response.status_code, 403)  # expects response status code to be 403 forbidden

        # positive test
        response = self.client.get(reverse('accounts:update_email', args=[self.user.id]), SERVER_NAME='localhost',
                                   secure=True)  # sends GET request to view with right user id
        self.assertEqual(response.status_code, 200)  # expects response status code to be 200 due to success
