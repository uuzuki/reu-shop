from .models import Category

def categories(request):
    return {'categories': Category.objects.filter(parent_category__isnull=True)}