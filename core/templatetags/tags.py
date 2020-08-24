from django import template
from django.contrib.auth.models import User
from random import shuffle

import arrow

from ..models import *

register = template.Library()


@register.simple_tag
def get_like_count(post):
    return UserProfile.objects.filter(liked_posts = post).count()


@register.simple_tag
def get_cart_count(user):
    return UserProfile.get_cart_count(user)


@register.simple_tag
def get_order_count(items):
    return items.filter(in_stock = True).count()


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
def get_num_remaining_links(post):
    return range(3 - post.links.count())


@register.simple_tag
def get_max_links():
    return range(3)


@register.simple_tag
def get_num_remaining_images(post):
    return range(3 - post.images.count())


@register.simple_tag
def get_max_images():
    return range(3)


@register.simple_tag
def get_notifications(user):
    return Notification.objects.filter(user = user.userprofile).order_by('-created')[:10]


@register.simple_tag
def get_active_order_items(user):
    order = Order.objects.filter(user=user, ordered=False)

    if order.exists():
        return OrderItem.objects.filter(order = order[0])

    return None


@register.simple_tag
def get_order_items(ref_code):
    order = Order.objects.filter(ref_code = ref_code)

    print(order)

    if order.exists():
        return OrderItem.objects.filter(order = order[0])

    return None


@register.simple_tag
def get_normal_time(datetime):
    return arrow.get(datetime).humanize()


@register.simple_tag
def get_comments(post):
    return PostComment.objects.filter(post = post)


@register.simple_tag
def get_latest_comment(post):
    return PostComment.objects.filter(post = post).latest('posted')


@register.simple_tag
def get_comment_count(post):
    return get_comments(post).count()


@register.simple_tag
def get_other_vendors(vendor):
    other_vendors = list(Vendor.objects.exclude(id = vendor.id)[:5])
    shuffle(other_vendors)

    return other_vendors