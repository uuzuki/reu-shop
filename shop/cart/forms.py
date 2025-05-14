# cart/forms.py
from django import forms
from zenitsu_shop.models import Product, Size

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=[(i, str(i)) for i in range(1, 21)], coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        if product:
            # Получаем доступные размеры для товара
            sizes = product.sizes.all()
            self.fields['size'] = forms.ModelChoiceField(
                queryset=sizes,
                empty_label="Выберите размер",
                required=True,
                label="Размер"
            )