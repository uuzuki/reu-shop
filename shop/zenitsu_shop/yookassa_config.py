from yookassa import Configuration
from django.conf import settings

def configure_yookassa():
    Configuration.configure(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)