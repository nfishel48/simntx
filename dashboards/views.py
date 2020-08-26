from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.template.loader import get_template
from django.contrib import messages
from django.utils import timezone

from core.models import *
from core.views import get_general_tags, get_vendors, can_create_promotion

from datetime import datetime, date, timedelta

from . import forms
from core import notifications

import stripe

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

        orders = Order.objects.filter(ordered = True, authorized = False, denied = False, cancelled = False, vendor = vendor)
        month_orders = Order.objects.filter(ordered = True, authorized = True, cancelled = False, vendor = vendor, ordered_date__date__month = datetime.today().month)

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


def order_action(request):
    print(request.POST)

    if request.POST:
        if 'action' in request.POST:
            if request.POST.get('action').lower() == 'approve':
                if 'ref_code' in request.POST:
                    order = Order.objects.filter(ref_code=request.POST.get('ref_code'))

                    if order.exists():
                        order = order[0]

                        products = [int(product) for product in request.POST.getlist('products')]

                        exclusions = OrderItem.objects.filter(order = order).exclude(id__in = products)

                        print('Exclusions: ' + str(exclusions))

                        return approve_order(request, order.ref_code, exclusions)
            elif request.POST.get('action').lower() == 'deny':
                #return deny_order(request, )
                pass

    return redirect('dashboards:vendor_page', page='approve_orders')


# Function : approve delivery
# This function is used by vendors to aprove a delivery and
# allow a driver too assigan the delivery
def approve_order(request, ref_code, exclusions=None):
    order = Order.objects.filter(ref_code=ref_code)

    if order.exists() and not order[0].authorized:
        order = order[0]

        if exclusions:
            for product in exclusions:
                product.in_stock = False
                product.save()

        order.authorized = True
        order.save()

        charge = chargeUser(request, order)

        if charge[0]:
            notifications.push(order.user,
                           'Order <span style = "font-family: Roboto-Medium;">#' + str(
                               order.ref_code) + '</span> has been approved by the vendor and is waiting for a driver. Your card has been charged.',
                           reverse('core:order', args=(order.ref_code,)))
        else:
            notifications.push(order.user,
                               'Order <span style = "font-family: Roboto-Medium;">#' + str(
                                   order.ref_code) + '</span> has been cancelled. <span style "color: var(--light-red)">' + charge[1] + '</span>',
                               reverse('core:order', args=(order.ref_code,)))

    return redirect('dashboards:vendor_page', page='approve_orders')


def deny_order(request, ref_code):
    order = Order.objects.filter(ref_code=ref_code)

    if order.exists() and not order[0].authorized:
        order = order[0]

        order.denied = True
        order.save()

        notifications.push(order.user,
                           'Order <span style = "font-family: Roboto-Medium;">#' + str(
                               order.ref_code) + '</span> has been denied by the vendor.',
                           reverse('core:order', args=(order.ref_code,)))

    return redirect('dashboards:vendor_page', page='approve_orders')


def chargeUser(request, order):
    warning = ''

    try:
        amount = int(order.get_total() * 100)

        charge = stripe.Charge.create(amount=amount, currency="usd", customer=order.user.userprofile.stripe_customer_id)

        payment = Payment()
        payment.stripe_charge_id = charge['id']
        payment.user = order.user
        payment.amount = charge['amount']
        payment.save()

        order.payment = payment
        order.save()

        return True, True
    except stripe.error.CardError as e:
        body = e.json_body

        err = body.get('error', {})

        warning = f"{err.get('message')}"
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        warning = "Rate limit error"
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        print(e)

        warning = "Invalid parameters"
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        warning = "Not authenticated"
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        warning = "Network error"
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        warning = "Something went wrong. You were not charged. Please try again."
    except Exception as e:
        # send an email to ourselves
        warning = "A serious error occurred. We have been notifed."

        print(e)

    return False, warning


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

    orders = Order.objects.filter(ordered=True, being_delivered=False, delivered=False, cancelled=False, authorized = True).exclude(user = request.user)

    data['orders'] = orders

    return render(request, 'dashboards/driver.html', data)


def driver_page(request, page):
    data = {}

    template = 'dashboards/driver/' + page + '.html'

    if not is_template(template):
        return redirect('dashboards:driver')

    if page == 'current':
        orders = Order.objects.filter(ordered = True, being_delivered = True, delivered = False, cancelled = False, driver = request.user.userprofile, authorized = True).exclude(user = request.user)

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


# View: Set Driver
# The function to attach a driver to an order
def set_driver(request, ref_code):
    order = Order.objects.filter(ref_code = ref_code)

    if order.exists() and not order[0].being_delivered:
        order = order[0]

        order.driver = request.user.userprofile
        order.being_delivered = True
        order.save()

        notifications.push(order.user,
                           'Order <span style = "font-family: Roboto-Medium;">#' + str(order.ref_code) + '</span> has been assigned a driver. Watch for your delivery!',
                           reverse('core:order', args=(order.ref_code,)))

    return redirect('dashboards:driver')


# View: Set Delivered
# The function to set an order as delivered
def set_delivered(request, ref_code):
    order = Order.objects.filter(ref_code = ref_code)

    if order.exists() and not order[0].delivered:
        order = order[0]
        order.being_delivered = False
        order.delivered = True
        order.delivered_date = timezone.now()
        order.save()

        notifications.push(order.user,
                           'Order <span style = "font-family: Roboto-Medium;">#' + str(order.ref_code) + '</span> has been delivered!',
                           reverse('core:order', args=(order.ref_code,)))

    return redirect('dashboards:driver')


def unset_driver(request, ref_code):
    order = Order.objects.filter(ref_code=ref_code)

    if order.exists() and not order[0].delivered:
        order = order[0]
        order.being_delivered = False
        order.driver = None
        order.save()

        notifications.push(order.user,
                           'Order <span style = "font-family: Roboto-Medium;">#' + str(
                               order.ref_code) + '</span> has been unassigned its driver. Its now waiting for another.',
                           reverse('core:order', args=(order.ref_code,)))

    return redirect('dashboards:driver')


def cancel_order(request, ref_code):
    order = Order.objects.filter(ref_code=ref_code)

    if order.exists() and not order[0].delivered:
        order = order[0]
        order.being_delivered = False
        order.delivered = False
        order.authorized = False
        order.cancelled = True
        order.save()

        notifications.push(order.user,
                           'Order <span style = "font-family: Roboto-Medium;">#' + str(
                               order.ref_code) + '</span> has been cancelled by the vendor.',
                           reverse('core:order', args=(order.ref_code,)))

    return redirect('dashboards:vendor')


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


def admin(request, month=date.today()):
    data = {}
    vendors = []

    total_balance = 0

    for vendor in Vendor.objects.all():
        month_balance = 0

        month_orders = Order.objects.filter(ordered=True, authorized=True, vendor=vendor,
                                        ordered_date__date__month=month.month, ordered_date__date__year=month.year)

        for order in month_orders.all():
            month_balance += order.get_vendor_keep()

        total_balance += month_balance

        if month_orders.count() > 0:
            vendors.append([vendor.title, month_orders.count(), month_balance])

    back_month = (month.replace(day=1) - timedelta(days=1))
    forward_month = (month.replace(day=1) + timedelta(days=40))

    data['vendors'] = vendors
    data['month'] = month.strftime('%B')
    data['year'] = month.year
    data['total_balance'] = total_balance

    data['back_month'] = back_month.strftime('%m%Y')
    data['forward_month'] = forward_month.strftime('%m%Y')

    data['back_name'] = back_month.strftime('%B')
    data['forward_name'] = forward_month.strftime('%B')

    return render(request, 'dashboards/admin.html', data)


def admin_past_month(request, month):
    return admin(request, month=date(int(month[-4:]), int(month[:-4]), 1))


# METHODS

def is_template(template):
    try:
        get_template(template)

        return True
    except:
        return False