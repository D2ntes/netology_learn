from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from .models import Product, Article


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
    # reviews = Review.objects.filter(product=prod).select_related('person').values('mark', 'review', 'person__username')
    context = {
        'product': prod,
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
                          'products': article.products.all().order_by('-amount_prod').values('id', 'title_prod',
                                                                                             'description_prod',
                                                                                             'amount_prod',
                                                                                             'image_prod')}

        list_articles.append(object_article)
    context = {
        'list_articles': list_articles,
        # 'list_types': nav()
    }

    return render(request, template, context)

