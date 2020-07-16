from django import forms
from django.db import models
from django.contrib.auth.models import User

from core.models import *

class EditVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['title', 'description', 'profile_image', 'cover_image', 'phone_number']

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']

class EditProductForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset = Tag.objects.all())

    class Meta:
        model = Item
        fields = ['title', 'description', 'image', 'price', 'discount_price', 'tags']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']

    def __init__(self, vendor, *args, **kwargs):
        self.vendor = vendor

        super(CreatePostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CreatePostForm, self).save(commit=False)
        instance.vendor = self.vendor

        if commit:
            instance.save()

        return instance

class CreateProductForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'discount_price', 'image', 'tags']

    def __init__(self, vendor, *args, **kwargs):
        self.vendor = vendor

        super(CreateProductForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CreateProductForm, self).save(commit=False)
        instance.vendor = self.vendor

        if commit:
            instance.save()

        return instance
