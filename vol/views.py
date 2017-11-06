from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Job


def index(request):
    return HttpResponse(render(request, 'vol/index.html'))


def about(request):
    return HttpResponse(render(request, 'vol/about.html'))


def results(request, location, interests):
    interests_queries = Q()
    for i in interests.split('+'):
        interests_queries |= Q(labels__name=i)

    locations_queries = Q()
    for l in location.split('+'):
        locations_queries |= Q(city=l)

    only_location_matches = False

    # All jobs
    jobs = Job.objects.filter()
    # TODO: assert we get any results

    # TODO: get rid of these ugly "all" workarounds
    if location == "all":
        matches = jobs.filter(interests_queries)
    elif interests == "all":
        matches = jobs.filter(locations_queries)

    else:
        # Give us all jobs that matched one or more of the locations AND one or more of the interests
        matches = jobs.filter(locations_queries & interests_queries)
        if len(matches) < 1:
            # Prefer location over interest
            # No matches for both locations and interests? Show location matches only
            only_location_matches = True
            matches = jobs.filter(locations_queries)
            # TODO assert there are any matches here

    location_matches = jobs.filter(locations_queries)
    interest_matches = jobs.filter(interests_queries)

    # Filter further down on results to find on location
    paginator = Paginator(matches, 25)  # Show 25 contacts per page

    match_count = len(matches)

    page = request.GET.get('page')

    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        matches = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        matches = paginator.page(paginator.num_pages)

    return render(request, 'vol/results.html', {
        'jobs': matches,
        'locations': location,
        'interests': interests,
        'location_matches': location_matches,
        'location_matches_count': len(location_matches),
        'interest_matches': interest_matches,
        'interests_matches_count': len(interest_matches),
        'matches': matches,
        'match_count': match_count,
        'match_count_on_page': len(matches),
        'only_location_matches': only_location_matches,
        'total_job_count': len(jobs)
    })


def job(request, uuid):
    job = get_object_or_404(Job, uuid=uuid)

    return render(request, 'vol/job.html', {'job': job})
