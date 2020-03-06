from django.contrib import admin
from .models import Product, Article, Vendor, Category, DetailOrder, Order
from .forms import Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title_prod', 'description_prod', 'amount_prod', 'category', 'vendor')


class ArticleHasProductsInline(admin.TabularInline):
    model = Article.products.through
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = Review
    list_display = ('title_art', 'description_art', 'published_at')
    inlines = [
        ArticleHasProductsInline,
    ]
    exclude = ('products',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title_category', 'get_vendors')


@admin.register(DetailOrder)
class DetailOrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount_do', 'order', 'person')


class OrderHasDetailsInline(admin.TabularInline):
    model = DetailOrder
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
    inlines = [
        OrderHasDetailsInline,
    ]
#
#
# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('mark', 'review', 'product', 'person')