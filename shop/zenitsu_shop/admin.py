from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

class CardAdmin(admin.ModelAdmin):
    list_display=('id','title','img_1','img_2','price')
class UserAdmin(admin.ModelAdmin):
    list_display=('id','username','email','password_hash','registration_date','last_login')
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','name','gender','parent_category')
class SizeAdmin(admin.ModelAdmin):
    list_display=('id','name','description')
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','name','description','img_1','price','stock_quantity','get_categories')
    list_filter = ['categories']  # Добавляет фильтр по категориям

    def get_categories(self, obj):
        return ", ".join(category.name for category in obj.categories.all())
    get_categories.short_description = 'Категории'

class ProductSizeAdmin(admin.ModelAdmin):
    list_display=('id','product','size', 'quantity')
    list_filter = ('product', 'size')
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display=('id','name','description','price','is_active','estimated_delivery_time')
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display=('id','name','description','is_active','requires_online','icon')

admin.site.register(Card, CardAdmin),
admin.site.register(User, UserAdmin),
admin.site.register(Size, SizeAdmin),
admin.site.register(Category, CategoryAdmin),
admin.site.register(Product, ProductAdmin),
admin.site.register(ProductSize, ProductSizeAdmin),
admin.site.register(DeliveryMethod, DeliveryMethodAdmin),
admin.site.register(PaymentMethod, PaymentMethodAdmin),
admin.site.register(PromoCode),
admin.site.register(Review),
admin.site.register(Wishlist),