# orders/forms.py
from django import forms
from zenitsu_shop.models import Order, PaymentMethod, DeliveryMethod

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'street', 'number_home', 'payment', 'delivery']
        widgets = {
            'city': forms.Select(choices=[('', 'Выберите город')] + [
                ('moscow', 'Москва'),
                ('saint_petersburg', 'Санкт-Петербург'),
                ('novosibirsk', 'Новосибирск'),
                ('ekaterinburg', 'Екатеринбург'),
                ('kazan', 'Казань'),
            ]),
            'payment': forms.Select(),
            'delivery': forms.RadioSelect(),  # Используем RadioSelect для доставки
        }

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['payment'].queryset = PaymentMethod.objects.all()
        self.fields['delivery'].queryset = DeliveryMethod.objects.all()
        # Устанавливаем первую доступную доставку как значение по умолчанию
        if DeliveryMethod.objects.exists():
            self.fields['delivery'].initial = DeliveryMethod.objects.first().pk
        for field in self.fields:
            self.fields[field].required = True