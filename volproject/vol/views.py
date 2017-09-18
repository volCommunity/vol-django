from django.http import HttpResponse, HttpResponseNotFound
from .models import Job, Organisation, Site, Labels
from django.template import loader
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse(render(request, 'vol/index.html'))

def about(request):
    return HttpResponse(render(request, 'vol/about.html'))

def results(request, subject, location, interests):
    # Ignoring subject for now, only using one location and interest
    # TODO: if zero results, did we find any with less tight?
    # conditions?
    location_matches = 0
    interest_matches = 0

    # Try all TODO: how do we build labels?
    # Is this, sort of, what we are looking for?
    # https://stackoverflow.com/questions/1841931/how-to-properly-query-a-manytomanyfield-for-all-the-objects-in-a-list-or-anothe
    # jobs = Job.objects.filter(city=location, labels=interests)
    jobs = Job.objects.filter(city=location)

    # If none found, did we find any that matches their interest?
    print("Amount of jobs %s" %len(jobs))
    amount_of_jobs = len(jobs)

    if amount_of_jobs < 1:
        jobs = Job.objects.filter(labels=interests)
        location_matches = len(jobs)

    amount_of_jobs = len(jobs)
    # Still none? Show them what is in their neighborhood
    if amount_of_jobs <1: #
        jobs = Job.objects.filter(city=location)
        interest_matches = len(jobs)

    amount_of_jobs = len(jobs)
    # Still no dice? Nothing we can do about his
    if amount_of_jobs < 1:
        # TODO: add better response here
        return HttpResponseNotFound('Job not found! Sad panda.')

    context = {
        'subject': subject,
        'location': location,
        'interests': interests,
        'location_matches': location_matches,
        'interest_matches': interest_matches,
        'job_count': len(jobs),
        'jobs': jobs
    }
    return HttpResponse(render(request, 'vol/results.html', context))


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
