from django.conf import settings
from django.db import models
# whenever new models are added the flollowing commands must be run
# python manage.py makemigrations
# python manage.py migrate

# ===Shopping cart and Item Backend Logic=====


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()

    def _str_(self):
        return self.title


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def _str_(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def _str_(self):
        return self.user.username

# ===End Shopping cart and Item logic
