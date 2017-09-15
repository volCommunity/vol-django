from django.db import models

# Create your models here.

class Labels(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Organisation(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=70)
    region = models.CharField(max_length=70)
    city = models.CharField(max_length=70)
    added = models.DateField('date added')

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    added = models.DateField('date added')

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)
    labels = models.ManyToManyField(Labels)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE) # One org per job
    site = models.ManyToManyField(Site)                                     # Possibly more sites per job
    country = models.CharField(max_length=70) # TODO: move to country table?
    region = models.CharField(max_length=70)  # TODO: move to region table?
    city = models.CharField(max_length=70)    # TODO: move to city table?
    added = models.DateField('date added')
    seen = models.IntegerField(default=0)     # How often someone has looked at job

    def __str__(self):
        return self.title
