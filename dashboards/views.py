from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.template.loader import get_template
from django.contrib import messages

from core.models import *
from core.views import get_general_tags, get_vendors, can_create_promotion

from datetime import datetime, date, timedelta

from . import forms


def vendor(request):
    data = {}
    
    vendor = get_vendors(request.user.userprofile)
    vendor.general_tags = get_general_tags(vendor)

    if request.method == 'POST':
        form = forms.EditVendorForm(request.POST, request.FILES, instance = vendor)

        print(request.POST)

        if form.is_valid():
            v = form.save()

            if v.address:
                v.address.delete()

            if v.hours:
                v.hours.delete()

            address = Address(street_address = request.POST['street_address'],
                              country = request.POST['country'],
                              zip = request.POST['zip'])

            hours = VendorHours(sunday_start = datetime.strptime(request.POST['sunday_start'], '%H:%S'),
                                  sunday_end = datetime.strptime(request.POST['sunday_end'], '%H:%S'),
                                  monday_start = datetime.strptime(request.POST['monday_start'], '%H:%S'),
                                  monday_end = datetime.strptime(request.POST['monday_end'], '%H:%S'),
                                  tuesday_start = datetime.strptime(request.POST['tuesday_start'], '%H:%S'),
                                  tuesday_end = datetime.strptime(request.POST['tuesday_end'], '%H:%S'),
                                  wednesday_start = datetime.strptime(request.POST['wednesday_start'], '%H:%S'),
                                  wednesday_end = datetime.strptime(request.POST['wednesday_end'], '%H:%S'),
                                  thursday_start = datetime.strptime(request.POST['thursday_start'], '%H:%S'),
                                  thursday_end = datetime.strptime(request.POST['thursday_end'], '%H:%S'),
                                  friday_start = datetime.strptime(request.POST['friday_start'], '%H:%S'),
                                  friday_end = datetime.strptime(request.POST['friday_end'], '%H:%S'),
                                  saturday_start = datetime.strptime(request.POST['saturday_start'], '%H:%S'),
                                  saturday_end = datetime.strptime(request.POST['saturday_end'], '%H:%S'))

            address.save()
            hours.save()

            v.hours = hours
            v.address = address

            v.save()
        else:
            print(form.errors)

    data['vendor'] = vendor

    return render(request, 'dashboards/vendor.html', data)


def vendor_page(request, page, month=date.today()):
    data = {}

    vendor = get_vendors(request.user.userprofile)

    template = 'dashboards/vendor/' + page + '.html'

    if not is_template(template):
        return redirect('dashboards:vendor')

    if page == 'posts':
        posts = Post.objects.filter(vendor = vendor).order_by('-posted')

        data['posts'] = posts
    elif page == 'products':
        print('products')

        products = Item.objects.filter(vendor = vendor)

        data['products'] = products
    elif page == 'approve_orders':
        month_balance = 0

        orders = Order.objects.filter(ordered = True, being_delivered = False, delivered = False, authorized = False, vendor = vendor)
        month_orders = Order.objects.filter(ordered = True, authorized = True, vendor = vendor, ordered_date__date__month = datetime.today().month)

        for order in month_orders.all():
            month_balance += order.get_vendor_keep()

        data['orders'] = orders
        data['num_orders'] = month_orders.count()
        data['amount_orders'] = month_balance
    elif page == 'past_orders':
        month_balance = 0

        month_orders = Order.objects.filter(ordered = True, authorized = True, vendor = vendor, ordered_date__date__month = month.month, ordered_date__date__year = month.year)

        for order in month_orders.all():
            month_balance += order.get_vendor_keep()

        back_month = (month.replace(day = 1) - timedelta(days = 1))
        forward_month = (month.replace(day = 1) + timedelta(days = 40))

        data['orders'] = month_orders
        data['month'] = month.strftime('%B')
        data['year'] = month.year
        data['num_orders'] = month_orders.count()
        data['amount_orders'] = month_balance

        data['back_month'] = back_month.strftime('%m%Y')
        data['forward_month'] = forward_month.strftime('%m%Y')

        data['back_name'] = back_month.strftime('%B')
        data['forward_name'] = forward_month.strftime('%B')
    elif page == 'promotions':
        promotions = list(StorePromotion.objects.filter(vendor = vendor)) + \
                     list(ProductPromotion.objects.filter(vendor = vendor)) + \
                     list(PostPromotion.objects.filter(vendor=vendor))

        data['promotions'] = promotions

    data['vendor'] = vendor

    print(template)

    return render(request, template, data)


def vendor_past_month(request, month):
    return vendor_page(request, 'past_orders', month=date(int(month[-4:]), int(month[:-4]), 1))


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

                if 'image' in request.POST:
                    images = request.POST.getlist('image')

                    for i in range(len(images)):
                        image = images[i]

                        if image != "" and image is not None:
                            if i < post.images.all().count():
                                post.images.all()[i].delete()

                            post_image = PostImage(image = image)

                            post_image.save()
                            post.images.add(post_image)

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

    vendor = get_vendors(request.user.userprofile)

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
        data['all_tags'] = GeneralTag.objects.all()

    data['vendor'] = vendor

    return render(request, template, data)


def create_page(request, page):
    data = {}

    vendor = get_vendors(request.user.userprofile)

    template = 'dashboards/vendor/create/' + page + '.html'

    if not is_template(template):
        return redirect('dashboards:vendor_page', page=page)

    if page == 'products':
        data['all_tags'] = GeneralTag.objects.all()
    elif page == 'promotions':


        data['all_products'] = Item.objects.filter(vendor = vendor)
        data['all_posts'] = Post.objects.filter(vendor = vendor)

    if request.method == 'POST':
        if page == 'posts':
            form = forms.CreatePostForm(vendor, request.POST, request.FILES)

            if form.is_valid():
                post = form.save()

                if 'link-urls' in request.POST:
                    names = request.POST.getlist('link-names')
                    urls = request.POST.getlist('link-urls')

                    for i in range(len(urls)):
                        name = names[i]
                        url = urls[i]

                        if url != "" and url is not None:
                            post_link = PostLink(link=url, title=name)

                            post_link.save()
                            post.links.add(post_link)

                if 'image' in request.FILES:
                    print(request.POST)
                    print(request.FILES)

                    for image in request.FILES.getlist('image'):
                        if image != "" and image is not None:
                            post_image = PostImage()
                            post_image.image.save(image.name, image)

                            post.images.add(post_image)

                post.save()
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
        elif page == 'promotions':
            if request.POST and can_create_promotion(vendor):
                if 'products' in request.POST:
                    products = Item.objects.filter(id__in = [int(id) for id in request.POST.getlist('products')], vendor = vendor)

                    promotion = StorePromotion(vendor = vendor)
                    promotion.save()

                    promotion.products.set(products)
                    promotion.save()
                elif 'product' in request.POST:
                    product = Item.objects.filter(id = int(request.POST.get('product')), vendor = vendor)

                    if product.exists():
                        promotion = ProductPromotion(vendor = vendor, product = product[0])
                        promotion.save()
                elif 'post' in request.POST:
                    post = Post.objects.filter(id = int(request.POST.get('post')), vendor=vendor)

                    if post.exists():
                        promotion = PostPromotion(vendor = vendor, post = post[0])
                        promotion.save()

        return redirect('dashboards:vendor_page', page=page)

    data['vendor'] = vendor

    return render(request, template, data)


def delete_page(request, page, id, **args):
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
    elif page == 'promotions':
        id, type = id.split('end')

        promotion = None

        if type == 'Store':
            promotion = StorePromotion.objects.filter(id=id)
        elif type == 'Product':
            promotion = ProductPromotion.objects.filter(id=id)
        elif type == 'Post':
            promotion = PostPromotion.objects.filter(id=id)

        if promotion.exists():
            promotion.delete()
        else:
            messages.info('Product was not able to be deleted')

    return redirect('dashboards:vendor_page', page=page)


def driver(request):
    data = {}

    orders = Order.objects.filter(ordered=True, being_delivered=False, delivered=False, authorized = True)#.exclude(user = request.user)

    data['orders'] = orders

    return render(request, 'dashboards/driver.html', data)


def driver_page(request, page):
    data = {}

    template = 'dashboards/driver/' + page + '.html'

    if not is_template(template):
        return redirect('dashboards:driver')

    if page == 'current':
        orders = Order.objects.filter(ordered = True, being_delivered = True, delivered = False, driver = request.user.userprofile, authorized = True)#.exclude(user = request.user)

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


def vendor_order(request, ref_code):
    order = Order.objects.filter(ref_code = ref_code)

    if order.exists():
        data = {}

        order = order[0]

        data['order'] = order

        return render(request, 'dashboards/vendor/order.html', data)
    else:
        return redirect('dashboards:vendor')


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