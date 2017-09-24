from django.http import HttpResponse, HttpResponseNotFound
from .models import Job, Organisation, Site, Labels
from django.db.models import Q
from django.template import loader
from django.shortcuts import render

def index(request):
    return HttpResponse(render(request, 'vol/index.html'))

def about(request):
    return HttpResponse(render(request, 'vol/about.html'))

def results(request, subject, location, interests):

    # TODO: split and downcase subject and location

    # Keep filtering down until all interests have been met, this won't be awesome if we have a lot of data
    # TODO: another approach, one that we should probably take it to order by things that matched *most* tags
    jobs = Job.objects.filter()
    print("Total jobs: %s" % len(jobs))
    interests_list = interests.split('+')
    interests_list = [interest.lower() for interest in interests_list]

    locations = location.split('+')
    locations = [location.lower() for location in locations]

    matched_interests= []
    unmatched_interests = []
    matched_intersection = 0

    while interests_list:
        # See which interests matches and which did not..
        interest = interests_list.pop()
        if jobs.filter(labels__name=interest):
            matched_interests.append(interest)
            jobs = jobs.filter(labels__name=interest)
        else:
            unmatched_interests.append(interest)

    matches = len(jobs)

    # Locations are a little different I guess, we want jobs for all the locations instead of filtering down
    # Q would be good here: Job.objects.filter(Q(city=city_one) | Q(city=city_two))
    q_objects = Q()
    while locations:
        q_objects |= Q(city=locations.pop())

    # print("Query now: ")
    # print(q_objects)
    location_matches = len(Job.objects.filter(q_objects))

    # print("Location matches: %s" % location_matches)
    # location_matches = len(Job.objects.filter(city=location))

    # TODO: find the intersetion, if there is none, pass all local jobs

    # Filter further down on results to find on location
    # print("Jobs # now: %s" % len(jobs))
    if len(jobs) > 0:
        print("Found jobs: %s" % len(jobs))
        if jobs.filter(q_objects): # There is an intersection, store it
            print("Filtering on location of found jobs results in :")
            print(jobs.filter(q_objects))
            jobs = jobs.filter(q_objects)
            if len(matched_interests) > 0: # This is a little ghetto
                matched_intersection =len(jobs)
                print("Matched intersection now: %s" % matched_intersection)

    context = {
        'subject': subject,
        'location': location,
        'interests': interests,
        'location_matches': location_matches,
        'matched_interests_count': len(matched_interests),
        'matched_interests': matched_interests,
        'unmatched_interests_count': len(unmatched_interests),
        'unmatched_interests': unmatched_interests,
        'matched_intersection': matched_intersection,
        'matches': matches,
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
