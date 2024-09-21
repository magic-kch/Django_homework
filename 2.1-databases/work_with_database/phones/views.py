from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    phones = Phone.objects.all()
    sort_by = request.GET.get('sort')
    if sort_by == 'name':
        phones = Phone.objects.order_by('name')
    elif sort_by == 'min_price':
        phones = Phone.objects.order_by('price')
    elif sort_by == 'max_price':
        phones = Phone.objects.order_by('-price')
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {'phone': Phone.objects.get(slug=slug)}
    return render(request, template, context)
