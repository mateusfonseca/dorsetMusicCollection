# CA2: Registration/Authentication
# CA3: Test and Security

"""
This file defines the accessible endpoints within the internal app accounts.
"""

from django.contrib.auth.views import LoginView
from django.urls import path

from .views import SignUpView, DetailView, DeleteView, UpdateEmailView

app_name = 'accounts'
urlpatterns = [
    path("login/", LoginView.as_view(redirect_authenticated_user=True), name="login"),  # log in view
    path("signup/", SignUpView.as_view(), name="signup"),  # sign up view
    path("<int:pk>/delete/", DeleteView.as_view(), name="delete"),  # delete view of specific user
    path("<int:pk>/detail/", DetailView.as_view(), name="detail"),  # details view of specific user
    path("<int:pk>/detail/email", UpdateEmailView.as_view(), name="update_email"),  # update email view of specific user
]
