
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from zenitsu_shop.views import *
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('product/<int:id>/', product, name='product'),
    path('list-card.html', list_card, name='list_card'),
    path('home.html', home, name='home'),
    path('<int:id>/', product, name='product'),
    path('products/', product_list, name='product_list'),
    path('blog.html', blog,),
    path('about.html', about, name='about'),
    path('delivery.html', delivery, name='delivery'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    re_path(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),
    re_path(r'^orders/', include(('orders.urls', 'orders'), namespace='orders')),
    re_path('index.html', include(('zenitsu_shop.urls', 'zenitsu_shop'), namespace='zenitsu_shop')),
    path('basket.html', basket),
    path('search/', product_search, name='product_search'),
    path('api/search/', search_api, name='search_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)