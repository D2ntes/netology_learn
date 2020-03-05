from .models import Category, DetailOrder
from django.contrib import auth


def category(request):
    return {"category_list": Category.objects.all()}


def nav_cart(request):
    if request.user.is_authenticated:
        person = auth.get_user(request)
        products_in_cart_cp = DetailOrder.objects.filter(person=person, order__isnull=True).prefetch_related(
            'product').count()
    else:
        products_in_cart_cp = 0

    return {'in_cart':products_in_cart_cp}

