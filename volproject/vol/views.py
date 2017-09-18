from django.http import HttpResponse, HttpResponseNotFound
from .models import Job, Organisation, Site, Labels
from django.template import loader
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse(render(request, 'vol/index.html'))

def about(request):
    return HttpResponse(render(request, 'vol/about.html'))

# TODO: add 404 templates
# TODO: use generated JSON for direct endpoints

def job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return HttpResponseNotFound('Job not found! Sad panda.')

    context = {
        'job': job,
    }
    return HttpResponse(render(request, 'vol/job.html', context))

def organisation(request, organisation_id):
    try:
        org = Organisation.objects.get(id=organisation_id)
    except Organisation.DoesNotExist:
        return HttpResponseNotFound('Organisation not found! Sad panda.')

    context = {
        'organisation': org,
    }
    return HttpResponse(render(request, 'vol/organisation.html', context))

def site(request, site_id):
    try:
        site = Site.objects.get(id=site_id)
    except Site.DoesNotExist:
        return HttpResponseNotFound('Site not found! Sad panda.')

    context = {
        'site': site,
    }
    return HttpResponse(render(request, 'vol/site.html', context))

def label(request, label_id):
    try:
        label = Labels.objects.get(id=label_id)
    except Labels.DoesNotExist:
        return HttpResponseNotFound('Label not found! Sad panda.')

    context = {
        'label': label,
    }

    return HttpResponse(render(request, 'vol/label.html', context))
