import django_filters
from .models import Product, Category, Size

class ProductFilter(django_filters.FilterSet):
    categories = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория'
    )
    sizes = django_filters.ModelMultipleChoiceFilter(
        queryset=Size.objects.all(),
        label='Размер'
    )
    price_min = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte', label='Минимальная цена'
    )
    price_max = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte', label='Максимальная цена'
    )

    class Meta:
        model = Product
        fields = ['categories', 'sizes', 'price_min', 'price_max']