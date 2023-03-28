# CA1: CRUD Application
# CA2: Registration/Authentication
# CA3: Test and Security

"""dorsetMusicCollection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# This file defines the accessible endpoints within the project.

urlpatterns = [
    path('polls/', include('polls.urls')),  # endpoints within polls
    # changed from 'admin' to 'management' for security purposes
    path('management/', admin.site.urls),  # endpoints within admin
    path("accounts/", include("accounts.urls")),  # endpoints within accounts
    path("accounts/", include("django.contrib.auth.urls")),
    # endpoints within admin related to authorization
    path('', TemplateView.as_view(template_name='home.html'), name='home'),  # website's home page
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),  # website's about page
    # website's page about the social media fingerprint exploit
    path('exploit/', TemplateView.as_view(template_name='exploit.html'), name='exploit'),
]
