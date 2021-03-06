from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from .models import Product, Article, Order, DetailOrder, Category
from django.core.paginator import Paginator


def product(request, id_product):
    if request.method == 'POST':
        person = auth.get_user(request)
        #     if 'feedback' in request.POST.keys() and 'mark' in request.POST.keys():
        #         id_product = request.POST['feedback']
        #         mark = request.POST['mark']
        #         description = request.POST['description']
        #         add_feedback(person, id_product, mark, description)
        if 'product' in request.POST.keys():
            id_product = request.POST['product']
            add_to_cart(person, id_product)

    template = 'product.html'
    prod = Product.objects.get(id=id_product)
    articles = prod.articles.all()
    list_articles = []
    for article in articles:
        object_article = {'title_art': article.title_art,
                          'description_art': article.description_art,
                          'id_art': article.id,
                          }

        list_articles.append(object_article)
    # reviews = Review.objects.filter(product=prod).select_related('person').values('mark', 'review', 'person__username')
    context = {
        'product': prod,
        'list_articles': list_articles,
        # 'reviews': reviews,
    }
    return render(request, template, context)


def index(request):
    if request.method == 'POST':
        if 'product' in request.POST.keys():
            id_product = request.POST['product']
            person = auth.get_user(request)
            add_to_cart(person, id_product)

    template = 'index.html'
    list_articles = []
    articles = Article.objects.all().prefetch_related('products').order_by('-published_at')
    for article in articles:
        object_article = {'title_art': article.title_art,
                          'description_art': article.description_art,
                          'products': article.products.order_by('-amount_prod')}

        list_articles.append(object_article)
    context = {'list_articles': list_articles,
               }
    return render(request, template, context)


def products(request):
    if request.method == 'POST':
        if 'product' in request.POST.keys():
            id_product = request.POST['product']
            person = auth.get_user(request)
            add_to_cart(person, id_product)
    template = 'products.html'

    list_products = []
    prods = Product.objects.all().prefetch_related('category', 'vendor').order_by('-title_prod')

    for prod in prods:
        object_product = {'id': prod.id,
                          'title_prod': prod.title_prod,
                          'description_prod': prod.description_prod,
                          'image_prod': prod.image_prod,
                          'category': prod.category,
                          'id_category': prod.category.id,
                          'vendor': prod.vendor,
                          }
        list_products.append(object_product)

    if request.GET.get('page'):
        page_number = int(request.GET.get('page'))
    else:
        page_number = 1
    p = Paginator(list_products, 2)
    if page_number in range(1, p.num_pages):
        stops_page = p.page(page_number)
    else:
        stops_page = p.page(p.num_pages)
    current_page = stops_page.number
    prev_page_url = f'?page={stops_page.previous_page_number()}' \
        if stops_page.has_previous() else None
    next_page_url = f'?page={stops_page.next_page_number()}' \
        if stops_page.has_next() else None

    return render(request, template, context={
        'list_products': stops_page,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })


def cart(request):
    template = 'cart.html'
    person = auth.get_user(request)
    if request.method == 'POST':
        if 'products_to_order' in request.POST.keys():
            new_order = Order.objects.create(status='Has been placed')
            DetailOrder.objects.filter(person=person, order__isnull=True).update(order=new_order)
        elif 'clear_order' in request.POST.keys():
            DetailOrder.objects.filter(person=person, order__isnull=True).delete()
            # DetailOrder.objects.create(person=person, order__isnull=False)

    products_in_cart = DetailOrder.objects.filter(person=person, order__isnull=True).prefetch_related('product').values(
        'amount_do', 'product__id', 'product__title_prod', 'product__description_prod', 'product__amount_prod',
        'product__image_prod')

    placed_orders = DetailOrder.objects.filter(person=person, order__isnull=False).prefetch_related('product').values(
        'product__title_prod', 'product__amount_prod', 'order_id', 'amount_do').order_by('order_id')

    context = {'products_in_cart': products_in_cart,
               'placed_orders': placed_orders,
               }
    return render(request, template, context)


def add_to_cart(person, id_product):
    prod = Product.objects.get(id=id_product)

    product_in_cart = DetailOrder.objects.filter(product_id=id_product, person=person, order__isnull=True).values()

    if product_in_cart.count() == 0:
        DetailOrder.objects.create(amount_do=0, product=prod, person=person)

    count_product_in_cart = product_in_cart[0]['amount_do']

    product_in_cart.update(amount_do=count_product_in_cart + 1)


def category(request, id_category):
    if request.method == 'POST':
        if 'product' in request.POST.keys():

            id_product = request.POST['product']
            person = auth.get_user(request)
            print(request.POST.keys())
            add_to_cart(person, id_product)

    template = 'category.html'
    cat = Category.objects.get(id=id_category)
    products = Product.objects.filter(category=cat.id)

    list_products = []
    for product in products:
        object_product = {'title_prod': product.title_prod,
                          'image_prod': product.image_prod,
                          'id_prod': product.id,
                          }
        list_products.append(object_product)

    context = {
        'category': cat,
        'list_products': list_products,
    }
    return render(request, template, context)


def about(request):
    template = 'about.html'
    info = information('name', 'description')
    context = {'company': info}
    return render(request, template, context)


def contact(request):
    template = 'contact.html'
    info = information('name', 'address', 'tel')
    context = {'company': info}
    return render(request, template, context)


def information(*keys):
    information_company = {
        'name': 'WebStore',
        'address': 'STREET, CITY, COUNTRY 000000',
        'tel': '+ 1235 2355 98',
        'description': 'To develop the website of the online store. '
                       'The client part of the service and the administration '
                       'interface must be implemented.',
        }

    return {key: information_company.get(key) for key in keys}
