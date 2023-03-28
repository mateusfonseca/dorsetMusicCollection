# CA1: CRUD Application

"""
This file defines the models that reflect the database's entities.
Each class is an entity and their properties are the tables' columns.
Instances of these classes are the database's entries, the tables' rows.
"""

import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):  # poll's question
    genre = models.CharField(max_length=50)  # question's genre
    year = models.IntegerField(default=0)  # question's year
    text = models.CharField(max_length=100)  # question's text as "What is the best <genre> album of <year>?"
    pub_date = models.DateTimeField('date published', default=timezone.now)  # question's pub_date

    def __str__(self):  # returns a string that describes the model
        return self.text  # returns "What is the best <genre> album of <year>?"

    @admin.display(  # controls how method behaves in the admin interface
        boolean=True,  # displays little mark, green if methods returns true, red if false
        ordering='pub_date',  # defaults the field pub_date as the ordering criteria
        description='Published recently?',  # title of descriptive column
    )
    def was_published_recently(self):  # method returns whether question has been published recently
        now = timezone.now()  # present time of when the function is called
        return now - datetime.timedelta(
            days=1) <= self.pub_date <= now  # returns whether the question was published in the last 24 hours


class Choice(models.Model):  # poll's choice (each one is an album)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # question to which choice belongs
    image = models.TextField(max_length=1000, default=None, blank=True, null=True)  # album's cover image
    title = models.CharField(max_length=100, default=None, blank=True, null=True)  # album's title
    artist = models.CharField(max_length=100, default=None, blank=True, null=True)  # album's artist
    year = models.IntegerField(default=None, blank=True, null=True)  # album's release year
    genres = models.TextField(max_length=500, default=None, blank=True, null=True)  # album's list of genres
    votes = models.IntegerField(default=0)  # number of votes the album has received
    country = models.CharField(max_length=50, default=None, blank=True, null=True)  # album's release country
    url = models.TextField(max_length=500, default=None, blank=True, null=True)  # album's url on Discogs website

    def __str__(self):  # returns a string that describes the model
        return f'{self.artist} - {self.title}'  # returns "<artist> - <title>"
