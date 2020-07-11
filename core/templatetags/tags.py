from django import template
from django.contrib.auth.models import User

import arrow

from ..models import *

register = template.Library()


@register.simple_tag
def get_cart_count(user):
    return UserProfile.get_cart_count(user)


@register.simple_tag
def get_notification_count(user):
    notis = Notification.objects.filter(user = user.userprofile, read = False)

    if notis.exists():
        return notis.count()

    return 0


@register.simple_tag
def get_follower_count(vendor):
    return UserProfile.objects.filter(following = vendor).count()


@register.simple_tag
def get_notifications(user):
    return Notification.objects.filter(user = user.userprofile).order_by('-created')


@register.simple_tag
def get_active_order_items(user):
    order = Order.objects.filter(user=user, ordered=False)

    if order.exists():
        return OrderItem.objects.filter(order = order[0])

    return None


@register.simple_tag
def get_order_items(ref_code):
    order = Order.objects.filter(ref_code = ref_code)

    if order.exists():
        return OrderItem.objects.filter(order = order[0])

    return None


@register.simple_tag
def get_normal_time(datetime):
    return arrow.get(datetime).humanize()