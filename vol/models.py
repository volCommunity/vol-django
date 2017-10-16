from django.db import models


# Create your models here.

class Labels(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Organisation(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=70)
    region = models.CharField(max_length=70)
    city = models.CharField(max_length=70)
    url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Site(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Job(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)
    labels = models.ManyToManyField(Labels)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)  # One org per job
    sites = models.ManyToManyField(Site)  # Possibly more sites per job
    country = models.CharField(max_length=70)  # TODO: move to country table?
    region = models.CharField(max_length=70, null=True)  # TODO: move to region table?
    city = models.CharField(max_length=70)  # TODO: move to city table?
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=200)
    seen = models.IntegerField(default=0)  # How often someone has looked at job

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
