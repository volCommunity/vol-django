from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from .models import Job


def index(request):
    return HttpResponse(render(request, 'vol/index.html'))


def about(request):
    return HttpResponse(render(request, 'vol/about.html'))


def results(request, location, interests):
    # Keep filtering down until all interests have been met, this won't be awesome if we
    # have a lot of data
    # TODO: another approach, one that we should probably take it to order by things that
    # matched *most* tags
    jobs = Job.objects.filter()
    interests_list = interests.split('+')
    locations = location.split('+')

    matched_interests = []
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

    # Locations are a little different I guess, we want jobs for all the locations instead of
    # filtering down
    q_objects = Q()
    while locations:
        q_objects |= Q(city=locations.pop())

    location_matches = len(Job.objects.filter(q_objects))

    # Filter further down on results to find on location
    if len(jobs) > 0:
        if jobs.filter(q_objects):  # There is an intersection, store it
            jobs = jobs.filter(q_objects)
            if len(matched_interests) > 0:  # This is a little ghetto
                matched_intersection = len(jobs)

    paginator = Paginator(jobs, 25)  # Show 25 contacts per page

    page = request.GET.get('page')

    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        jobs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        jobs = paginator.page(paginator.num_pages)

    return render(request, 'vol/results.html', {
        'jobs': jobs,
        'locations': location,
        'interests': interests,
        'location_matches': location_matches,
        'matched_interests_count': len(matched_interests),
        'matched_interests': matched_interests,
        'unmatched_interests_count': len(unmatched_interests),
        'unmatched_interests': unmatched_interests,
        'matched_intersection': matched_intersection,
        'matches': matches,
        'job_count': len(jobs)
    })
