from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser


LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Tag(models.Model):
    name = models.CharField(max_length = 20)
    color = models.CharField(max_length = 7)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(max_length=100)
    owner = models.ForeignKey('UserProfile', on_delete = models.CASCADE)
    zip_code = models.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:vendor", kwargs={
            'slug': self.slug
        })

    def get_vendor_owner(self):
        return self.owner


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 50, blank = False, null = False)
    last_name = models.CharField(max_length = 50, blank = False, null = False)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    vendor_owner = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username

    def get_user(self):
        return self.user

    @classmethod
    def get_cart_count(cls, user):
        order = Order.objects.filter(user = user, ordered = False)

        if order.exists():
            return OrderItem.objects.filter(order = order[0]).count()

        return 0


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name = 'item')
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey('Order', null = True, on_delete = models.CASCADE, related_name = 'order')

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()

        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    driver = models.ForeignKey('UserProfile', related_name='driver', on_delete=models.SET_NULL, default=1, blank=True, null=True)

    ordered_date = models.DateTimeField(null = True)
    delivered_date = models.DateTimeField(null = True)

    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)

    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)

    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.get_items(self):
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    
    def get_ref_code(self):
        return self.ref_code

    def get_shipping(self):
        return self.shipping_address

    def get_absolute_url(self):
        return reverse("core:order", kwargs={
            'ref_code': self.ref_code
        })

    @classmethod
    def get_items(cls, order):
        return OrderItem.objects.filter(order = order)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


class Post(models.Model):
    text = models.CharField(max_length = 500, null = False, blank = False)
    vendor = models.ForeignKey('Vendor', on_delete = models.CASCADE, related_name = 'vendor', null = False, blank = False)
    posted = models.DateTimeField(auto_now=True)
    links = models.ManyToManyField('PostLink', blank = True)

    def __str__(self):
        return self.vendor.title + ": " + self.text[:50]

    def get_title(self):
        return self.text[:50]


class PostImage(models.Model):
    image = models.ImageField()
    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = 'post')


class PostLink(models.Model):
    link = models.URLField()


class Notification(models.Model):
    user = models.ForeignKey('UserProfile', on_delete = models.CASCADE, related_name = 'notification_user')
    text = models.CharField(max_length = 100)
    link = models.CharField(max_length = 100)
    created = models.DateTimeField(auto_now = True)
    read = models.BooleanField(default = False)


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

