from django.shortcuts import render
from phones.models import Phone


def show_catalog(request):
    template = 'catalog.html'
    phones = Phone.objects.all()
    context = {
        'phones': phones
    }
    return render(
        request,
        template,
        context
    )
