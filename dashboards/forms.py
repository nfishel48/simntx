from django import forms
from django.db import models
from django.contrib.auth.models import User

from core.models import *

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']

class EditProductForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset = Tag.objects.all())

    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'discount_price', 'tags']