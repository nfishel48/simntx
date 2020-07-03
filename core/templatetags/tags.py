from django import template
from django.contrib.auth.models import User

from ..models import *

register = template.Library()

@register.simple_tag
def get_cart_count(user):
	return UserProfile.get_cart_count(user)


@register.simple_tag
def get_order_items(user):
    order = Order.objects.filter(user=user)

    if order.exists():
        return OrderItem.objects.filter(order = order[0])

    return None


@register.simple_tag
def get_profile(user):
    return UserProfile.objects.get(user = user)