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

    if request.method == 'POST':
        form = forms.EditVendorForm(request.POST, request.FILES, instance = vendor)

        if form.is_valid():
            v = form.save()
        else:
            print(form.errors)

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

                print(request.POST)

                if 'link-urls' in request.POST:
                    post.links.all().delete()

                    names = request.POST.getlist('link-names')
                    urls = request.POST.getlist('link-urls')

                    for i in range(len(urls)):
                        name = names[i]
                        url = urls[i]

                        if url != "" and url is not None:
                            print(name + ' // ' + url)

                            post_link = PostLink.objects.filter(link = url, title = name)

                            if post_link.exists():
                                post_link = post_link[0]
                            else:
                                post_link = PostLink(link = url, title = name)

                            post_link.save()
                            post.links.add(post_link)

                post.save()
            else:
                print(form.errors)
        elif page == 'products':
            form = forms.EditProductForm(request.POST, request.FILES, instance = Item.objects.get(id=id))

            if form.is_valid():
                product = form.save()
            else:
                print(form.errors)

        return redirect('dashboards:vendor_page', page=page)

    vendor = Vendor.objects.get(owner=request.user.userprofile)

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


def create_page(request, page):
    data = {}

    vendor = Vendor.objects.get(owner=request.user.userprofile)

    template = 'dashboards/vendor/create/' + page + '.html'

    if not is_template(template):
        return redirect('dashboards:vendor_page', page=page)

    if page == 'products':
        data['all_tags'] = Tag.objects.all()

    if request.method == 'POST':
        if page == 'posts':
            form = forms.CreatePostForm(vendor, request.POST)

            if form.is_valid():
                post = form.save()
            else:
                print(form.errors)
        elif page == 'products':
            form = forms.CreateProductForm(vendor, request.POST, request.FILES)

            if form.is_valid():
                product = form.save()
                form.save_m2m()
            else:
                data['form'] = form

                return render(request, template, data)

        return redirect('dashboards:vendor_page', page=page)

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
    data = {}

    orders = Order.objects.filter(ordered=True, being_delivered=False, delivered=False)#.exclude(user = request.user)

    data['orders'] = orders

    return render(request, 'dashboards/driver.html', data)


def driver_page(request, page):
    data = {}

    template = 'dashboards/driver/' + page + '.html'

    if not is_template(template):
        return redirect('dashboards:driver')

    if page == 'current':
        orders = Order.objects.filter(ordered = True, being_delivered = True, delivered = False, driver = request.user.userprofile)#.exclude(user = request.user)

        data['orders'] = orders
       
    elif page == 'completed':
        orders = Order.objects.filter(ordered = True, being_delivered = False, delivered = True, driver = request.user.userprofile)

        data['orders'] = orders

    elif page == 'products':
        print('products')

        products = Item.objects.filter(vendor = vendor)

        data['products'] = products
        print('products')

    data['vendor'] = vendor

    print(template)

    return render(request, template, data)


def order(request, ref_code):
    order = Order.objects.filter(ref_code = ref_code)

    if order.exists():
        data = {}

        order = order[0]

        data['order'] = order

        return render(request, 'dashboards/driver/order.html', data)
    else:
        return redirect('dashboards:driver')


# METHODS

def is_template(template):
    try:
        get_template(template)

        return True
    except:
        return False