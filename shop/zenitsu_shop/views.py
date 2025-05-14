# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from cart.forms import CartAddProductForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages
import logging
from django.db.models import Q, Func
from django.conf import settings
import re
import json
from .filters import ProductFilter
from django.db.models.functions import Lower

# Create your views here.

def account(request):
    return render(request, "zenitsu_shop/account.html")
def about(request):
    return render(request, "zenitsu_shop/about.html")
def delivery(request):
    return render(request, "zenitsu_shop/delivery.html")

logger = logging.getLogger(__name__)

def index(request):
    # Получаем категории
    categories = {
        'new': None,
        'tshirts': None,
        'sweatshirts': None,
        'jeans': None,
    }
    
    try:
        categories['new'] = Category.objects.get(name="Новинки")
        logger.info("Категория 'Новинки' найдена")
    except Category.DoesNotExist:
        logger.warning("Категория 'Новинки' не найдена")
    
    try:
        categories['tshirts'] = Category.objects.get(name="Футболки")
        logger.info("Категория 'Футболки' найдена")
    except Category.DoesNotExist:
        logger.warning("Категория 'Футболки' не найдена")
    
    try:
        categories['sweatshirts'] = Category.objects.get(name="Свитшоты")
        logger.info("Категория 'Свитшоты' найдена")
    except Category.DoesNotExist:
        logger.warning("Категория 'Свитшоты' не найдена")
    
    try:
        categories['jeans'] = Category.objects.get(name="Джинсы")
        logger.info("Категория 'Джинсы' найдена")
    except Category.DoesNotExist:
        logger.warning("Категория 'Джинсы' не найдена")

    # Получаем товары для каждой категории
    products = {
        'new': Product.objects.filter(categories=categories['new'], is_active=True)[:8] if categories['new'] else Product.objects.none(),
        'tshirts': Product.objects.filter(categories=categories['tshirts'], is_active=True)[:8] if categories['tshirts'] else Product.objects.none(),
        'sweatshirts': Product.objects.filter(categories=categories['sweatshirts'], is_active=True)[:8] if categories['sweatshirts'] else Product.objects.none(),
        'jeans': Product.objects.filter(categories=categories['jeans'], is_active=True)[:8] if categories['jeans'] else Product.objects.none(),
    }

    # Логируем количество товаров
    for key, product_list in products.items():
        logger.info(f"Категория {key}: {product_list.count()} товаров")

    context = {
        'new': products['new'],
        'tshirts': products['tshirts'],
        'sweatshirts': products['sweatshirts'],
        'jeans': products['jeans'],
    }
    
    return render(request, 'zenitsu_shop/index.html', context)

def product_list(request):
    category_id = request.GET.get('category')
    gender = request.GET.get('gender')
    
    products = Product.objects.all()
    categories = Category.objects.filter(parent_category__isnull=True)
    
    if category_id:
        products = products.filter(category__id=category_id)
    
    if gender:
        products = products.filter(category__gender=gender)
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/list.html', context)

def list_card(request):
    # Получаем параметры из GET-запроса
    sort_option = request.GET.get('sort', 'newest')
    category_id = request.GET.get('category')
    
    # Инициализация фильтра
    products = Product.objects.filter(is_active=True)
    
    # Применяем фильтр по категории
    if category_id:
        products = products.filter(categories__id=category_id)
    
    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_products = product_filter.qs

    # Применение сортировки
    if sort_option == 'newest':
        filtered_products = filtered_products.order_by('-created_at')
    elif sort_option == 'price_asc':
        filtered_products = filtered_products.order_by('price')
    elif sort_option == 'price_desc':
        filtered_products = filtered_products.order_by('-price')
    elif sort_option == 'sale':
        filtered_products = filtered_products.filter(discount__gt=0).order_by('-discount')
    
    # Получение всех категорий и размеров для фильтров
    categories = Category.objects.filter(parent_category__isnull=True)  # Исправлено parent_categories на parent_category
    sizes = Size.objects.all()

    # Ограничение для отображения топ-продуктов
    top_products = filtered_products[:5]

    context = {
        'top_products': top_products,
        'sort_option': sort_option,
        'products': filtered_products,
        'categories': categories,
        'sizes': sizes,
        'filter': product_filter,
        'current_category_id': int(category_id) if category_id else None,
    }
    return render(request, 'zenitsu_shop/list-card.html', context)

def product(request, id):
    product = get_object_or_404(Product, id=id, is_active=True)
    cart_product_form = CartAddProductForm(product=product)  # Передаём продукт в форму
    
    # Получаем случайные товары (исключая текущий товар)
    random_products = Product.objects.filter(
        is_active=True
    ).exclude(id=id).order_by('?')[:4]
    
    return render(request, 'zenitsu_shop/product.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'random_products': random_products
    })
    
def blog(request):
    return render(request, 'zenitsu_shop/blog.html')
def account(request):
    return render(request, 'zenitsu_shop/account.html')
def basket(request):
    return render(request, 'zenitsu_shop/basket.html')
def home(request):
    return render(request,"zenitsu_shop/home.html")

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация прошла успешно!')
        return response

logger = logging.getLogger(__name__)

class UpperCase(Func):
    function = 'UPPER'

def product_filter(request):
    queryset = Product.objects.filter(is_active=True)
    product_filter = ProductFilter(request.GET, queryset=queryset)
    
    categories = Category.objects.all()
    sizes = Size.objects.all()
    
    context = {
        'filter': product_filter,
        'products': product_filter.qs,
        'categories': categories,
        'sizes': sizes,
        'top_products': product_filter.qs[:12],
    }
    
    return render(request, 'shop/list-card.html', context)

def product_search(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse([], safe=False)
    
    upper_query = query.upper()
    
    products = Product.objects.annotate(
        upper_name=UpperCase('name'),
        upper_description=UpperCase('description')
    ).filter(
        Q(upper_name__icontains=upper_query) | 
        Q(upper_description__icontains=upper_query),
        is_active=True
    )[:10]
    
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'url': product.get_absolute_url(),
            'image': product.img_1 or '/static/default-product.png'
        })

    return JsonResponse(data, safe=False)

def search_api(request):
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        if len(query) >= 2:
            lower_query = query.lower()
            # Проверяем, есть ли категория с таким названием
            try:
                category = Category.objects.annotate(
                    lower_name=Lower('name')
                ).get(lower_name__icontains=lower_query)
                # Если категория найдена, приоритет товарам из этой категории
                products = Product.objects.filter(
                    categories=category,
                    is_active=True
                ).annotate(
                    lower_name=Lower('name'),
                    lower_description=Lower('description')
                )[:10]
            except Category.DoesNotExist:
                # Обычный поиск по названию, описанию и категории
                products = Product.objects.annotate(
                    lower_name=Lower('name'),
                    lower_description=Lower('description'),
                    lower_category_name=Lower('categories__name')
                ).filter(
                    Q(lower_name__icontains=lower_query) |
                    Q(lower_description__icontains=lower_query) |
                    Q(lower_category_name__icontains=lower_query),
                    is_active=True
                ).distinct()[:10]
            
            results = [
                {
                    'id': p.id,
                    'name': p.name,
                    'price': str(p.price),
                    'img_1': p.img_1 if p.img_1 else '/static/default-product.png',
                    'url': f'/{p.id}/',
                    'categories': [cat.name for cat in p.categories.all()]
                }
                for p in products
            ]
            return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


logger = logging.getLogger(__name__)

def my_view(request):
    logger.debug("Это сообщение уровня DEBUG")
    logger.info("Это сообщение уровня INFO")
    logger.warning("Это предупреждение!")
    logger.error("Это ошибка!")
    
    try:
        result = 10 / 0
    except Exception as e:
        logger.exception("Произошла ошибка: %s", str(e))
    
    return HttpResponse("Проверьте логи в консоли!")

def catalog_view(request):
    categories = Category.objects.filter(parent_categories__isnull=True)  # Только родительские категории
    return render(request, 'your_template.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)  # Fetch a single category
    products = Product.objects.filter(categories=category)  # Use the renamed 'categories' field
    return render(request, 'zenitsu_shop/category_detail.html', {
        'category': category,  # Pass the single category
        'products': products
    })
