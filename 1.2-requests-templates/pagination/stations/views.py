from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv

from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    paginator = Paginator(get_context(BUS_STATION_CSV), 10)
    page = paginator.get_page(int(request.GET.get('page', 1)))
    context = {
        'bus_stations': get_context(BUS_STATION_CSV)[(page.number - 1) * 10:page.number * 10],
        'page': page,
    }
    return render(request, 'stations/index.html', context)


def get_context(file):
    values = []
    with open(file, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            values.append(row)
    return values
