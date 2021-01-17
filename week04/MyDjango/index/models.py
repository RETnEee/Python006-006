from django.db import models

class Film(models.Model):
    name = models.CharField(max_length=30)
    director = models.CharField(max_length=30)
    actor = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    time = models.DateTimeField()


class Comment(models.Model):
    filmname = models.TextField()
    rank = models.IntegerField()
    author = models.CharField(max_length=20)
    time = models.DateTimeField()
    title = models.TextField()
    text = models.TextField()