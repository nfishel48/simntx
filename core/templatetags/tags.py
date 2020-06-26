from django import template
from django.contrib.auth.models import User

from ..models import *

register = template.Library()

@register.simple_tag
def get_profile(user):
    return UserProfile.objects.get(user = user)