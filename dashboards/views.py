from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib import messages

from core.models import *
from core.views import get_tags

from . import forms


def vendor(request):
    data = {}

    vendor = Vendor.objects.get(owner = UserProfile.objects.get(user = request.user))

    vendor.tags = get_tags(vendor)

    data['vendor'] = vendor

    return render(request, 'dashboards/vendor.html', data)


def vendor_page(request, page):
    data = {}

    profile = request.user.userprofile
    vendor = Vendor.objects.get(owner = profile)

    template = 'dashboards/vendor/' + page + '.html'

    if not is_template(template):
        return redirect('dashboards:vendor')

    if page == 'posts':
        posts = Post.objects.filter(vendor = vendor)

        data['posts'] = posts
    elif page == 'products':
        print('products')

        products = Item.objects.filter(vendor = vendor)

        data['products'] = products
        print('products')

    data['vendor'] = vendor

    print(template)

    return render(request, template, data)


def edit_page(request, page, id):
    data = {}

    if request.method == 'POST':
        if page == 'posts':
            form = forms.EditPostForm(request.POST)

            if form.is_valid():
                post = Post.objects.get(id = id)
                post.text = form.cleaned_data['text']

                post.save()
            else:
                print(form.errors)
        elif page == 'products':
            form = forms.EditProductForm(request.POST)

            if form.is_valid():
                product = Item.objects.get(id=id)
                product.title = form.cleaned_data['title']
                product.description = form.cleaned_data['description']
                product.price = form.cleaned_data['price']
                product.discount_price = form.cleaned_data['discount_price']
                product.tags.set(form.cleaned_data['tags'])

                product.save()
            else:
                print(form.errors)

        return redirect('dashboards:vendor_page', page=page)

    profile = request.user.userprofile
    vendor = Vendor.objects.get(owner=profile)

    template = 'dashboards/vendor/edit/' + page + '.html'

    if not is_template(template):
        return redirect('dashboards:vendor_page', page=page)

    if page == 'posts':
        post = Post.objects.filter(id = id)

        if not post.exists():
            return redirect('dashboards:vendor_page', page=page)

        data['post'] = post[0]
    elif page == 'products':
        product = Item.objects.filter(id=id)

        if not product.exists():
            return redirect('dashboards:vendor_page', page=page)

        data['product'] = product[0]
        data['all_tags'] = Tag.objects.all()

    data['vendor'] = vendor

    return render(request, template, data)


def delete_page(request, page, id):
    if page == 'posts':
        post = Post.objects.filter(id = id)

        if post.exists():
            post.delete()
        else:
            messages.info('Post was not able to be deleted')
    elif page == 'products':
        product = Item.objects.filter(id=id)

        if product.exists():
            product.delete()
        else:
            messages.info('Product was not able to be deleted')

    return redirect('dashboards:vendor_page', page=page)


def driver(request):
    return render(request, 'dashboards/driver.html')

# METHODS

def is_template(template):
    try:
        get_template(template)

        return True
    except:
        return False