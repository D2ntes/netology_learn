from django.contrib import admin
from .models import Product, Article#, Type, Subtype, Article,  DetailOrder, Order, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title_prod', 'description_prod', 'amount_prod')#, 'type', 'subtype')


class ArticleHasProductsInline(admin.TabularInline):
    model = Article.products.through
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title_art', 'description_art', 'published_at')
    inlines = [
        ArticleHasProductsInline,
    ]
    exclude = ('products',)





# @admin.register(Type)
# class TypeAdmin(admin.ModelAdmin):
#     extra = 1
#
#
# @admin.register(Subtype)
# class SubtypeAdmin(admin.ModelAdmin):
#     list_display = ('title_subt', 'type')
#
#

#
#




# @admin.register(DetailOrder)
# class DetailOrderAdmin(admin.ModelAdmin):
#     list_display = ('product', 'amount_do', 'order', 'person')
#
#
# class OrderHasDetailsInline(admin.TabularInline):
#     model = DetailOrder
#     extra = 0
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'status')
#     inlines = [
#         OrderHasDetailsInline,
#     ]
#
#
# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('mark', 'review', 'product', 'person')