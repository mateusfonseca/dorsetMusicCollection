# CA1: CRUD Application

"""
This file defines the accessible endpoints within the app polls.
"""

from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # app's home view
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),  # details view of specific poll
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),  # results view of specific poll
    path('<int:question_id>/vote/', views.vote, name='vote'),  # submit vote to specific poll
    path('create', views.CreateView.as_view(), name='create'),  # create new poll view
    path('create', views.CreateView.post, name='create_selected'),  # submit newly created poll
]
