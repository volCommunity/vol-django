import uuid
from django.db import models


# Create your models here.

class Labels(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


class Organisation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=4000, blank=True)
    country = models.CharField(max_length=70)
    region = models.CharField(max_length=70)
    city = models.CharField(max_length=70)
    url = models.CharField(max_length=2083)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


class Site(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=2083, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


class Job(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    labels = models.ManyToManyField(Labels)
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True)  # Not all jobs have a known org
    sites = models.ManyToManyField(Site)  # Possibly more sites per job
    country = models.CharField(max_length=70)  # TODO: move to country table
    region = models.CharField(max_length=70, null=True)  # TODO: move to region table? TODO: don't use null for char
    city = models.CharField(max_length=70)  # TODO: move to city table
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=2083, unique=True)
    seen = models.IntegerField(default=0)  # How often someone has looked at job

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']
