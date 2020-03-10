from .models import Category, DetailOrder
from django.contrib import auth
from django.db.models import Sum


def category(request):
    categories = Category.objects.all()
    category_list = []
    for category in categories:
        category_list.append({'id_category': category.id, 'title_category': category.title_category})
    return {"category_list": category_list}


def nav_cart(request):
    in_cart = 0
    if request.user.is_authenticated:
        person = auth.get_user(request)

        products_in_cart = DetailOrder.objects.filter(person=person, order__isnull=True).annotate(
            amount_product=Sum('amount_do'))

        for product_in_cart in products_in_cart:
            in_cart += product_in_cart.amount_product

    return {'in_cart': in_cart}

