from django.shortcuts import render
from .models import EventFilter, Event, Category
from .forms import CreateEventForm
from django.http import JsonResponse


def event_list(request):
    filter = EventFilter(request.GET, queryset=Event.objects.all())
    return render(request, 'events_list.html', {'filter': filter})


def all_markers(request):
    if request.is_ajax():
        response = list()
        for event in Event.objects.filter():
            response.append([event.wid_location, event.len_location])
        return JsonResponse({'resp': response[1:]})


def ajax_event(request):
    return render(request, 'ajax_event.html')


def map(request):
    categories = Category.objects.order_by('title').all()

    return render(request, 'map.html', {'categories': categories})


def get_create_form(request):
    return render(request, 'createEvent.html')


def get_marker_content(request):
    len_location = request.POST.get('len_location')
    wid_location = request.POST.get('wid_location')

    event = Event.objects.filter(len_location=len_location, wid_location=wid_location).first()
    if event:
        return render(request, 'ajax_event.html', {'event': event})


def add_event(request):
    # create_form = CreateEventForm(request.POST)

    # if create_form.is_valid():
    #     new_event = create_form.save(commit=False)
    #     new_event.location = request.POST.get('location')

    title = request.POST.get('title')
    short_description = request.POST.get('short_description')
    description = request.POST.get('description')
    len_location = request.POST.get('len_location')
    wid_location = request.POST.get('wid_location')

    new_event = Event(title=title, short_description=short_description, description=description,
                      len_location=len_location, wid_location=wid_location, author=request.user)
    new_event.save()

    return JsonResponse({'status': 'success', 'soc_id': request.user.social_id, 'description': description})
