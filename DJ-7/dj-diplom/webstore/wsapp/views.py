from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from .models import Product, Article
from django.core.paginator import Paginator


def product(request, id_product):
    person = auth.get_user(request)
    # if request.method == 'POST':
    #     if 'feedback' in request.POST.keys() and 'mark' in request.POST.keys():
    #         id_product = request.POST['feedback']
    #         mark = request.POST['mark']
    #         description = request.POST['description']
    #         add_feedback(person, id_product, mark, description)
    #     if 'product' in request.POST.keys():
    #         id_product = request.POST['product']
    #         add_to_cart(person, id_product)

    template = 'product.html'
    prod = Product.objects.get(id=id_product)
    articles = prod.articles.all()
    list_articles = []
    for article in articles:
        object_article = {'title_art': article.title_art,
                          'description_art': article.description_art
                          }

        list_articles.append(object_article)
    # reviews = Review.objects.filter(product=prod).select_related('person').values('mark', 'review', 'person__username')
    context = {
        'product': prod,
        'list_articles': list_articles

        # 'reviews': reviews,
        # 'list_types': nav()
    }
    return render(request, template, context)


def index(request):
    # if request.method == 'POST':
    #     if 'product' in request.POST.keys():
    #         id_product = request.POST['product']
    #         person = auth.get_user(request)
    #         add_to_cart(person, id_product)
    template = 'index.html'
    list_articles = []
    articles = Article.objects.all().prefetch_related('products').order_by('-published_at')
    for article in articles:
        object_article = {'title_art': article.title_art,
                          'description_art': article.description_art,
                          'products': article.products.order_by('-amount_prod')}

        list_articles.append(object_article)
    context = {
        'list_articles': list_articles,
        # 'list_types': nav()
    }

    return render(request, template, context)


def products(request):
    # if request.method == 'POST':
    #     if 'product' in request.POST.keys():
    #         id_product = request.POST['product']
    #         person = auth.get_user(request)
    #         add_to_cart(person, id_product)
    template = 'products.html'

    list_products = []
    prods = Product.objects.all().order_by('-title_prod')
    for prod in prods:
        object_product = {'id': prod.id,
                          'title_prod': prod.title_prod,
                          'description_prod': prod.description_prod,
                          'image_prod': prod.image_prod,
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
