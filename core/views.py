from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from allauth.account.views import PasswordChangeView
from allauth.account.forms import ChangePasswordForm

from .forms import *
from .models import *

from . import notifications

import random
import string
import stripe
import arrow

stripe.api_key = settings.STRIPE_SECRET_KEY

load_amount = 10

# View: Index
# The view that redirects to the front page
def index(request):
    return redirect('/feed')

# View: Feed
# The page for posts from vendors you follow
def feed(request):
    posts = Post.objects.all()

    for post in posts:
        post.posted = arrow.get(post.posted).humanize()  # Convert DateTime to human-friendly message

    return render(request, 'feed.html', {
        'posts': posts,
    })


# View: Store
# The store showing all vendors and products
def store(request):
    vendors = Vendor.objects.all()[:10]
    products = Item.objects.all()[:10]
    food = Item.objects.filter(tags = Tag.objects.get(name = 'food'))[:10]

    for vendor in vendors:
        vendor.tags = get_tags(vendor.id)

    return render(request, 'store.html', {
        'vendors': vendors,
        'products': products,
        'food': food,
    })


# View: Vendor
# The page for a specific vendor
def vendor(request, slug):
    return redirect('core:vendor_store', slug=slug)


# View: Vendor Feed
# The tab on a vendors page that shows all of their posts
def vendor_feed(request, slug):
    vendor = Vendor.objects.get(slug=slug)

    posts = Post.objects.all()

    for post in posts:
        post.posted = arrow.get(post.posted).humanize()

    return render(request, 'vendor_feed.html', {
        'vendor': vendor,
        'posts': posts,
    })


# View: Vendor Store
# The store showing all the vendors products
def vendor_store(request, slug):
    vendor = Vendor.objects.get(slug=slug)
    products = Item.objects.filter(vendor=vendor)

    vendor.tags = get_tags(vendor.id)

    data = search(request, [Q(vendor=vendor)])  # Only searches items from this vendor

    data['vendor'] = vendor
    data['products'] = products

    return render(request, 'vendor_store.html', data)


# View: Product
# The page for a specific product
def product(request, slug):
    product = Item.objects.get(slug = slug)
    other_products = Item.objects.filter(vendor = product.vendor)

    return render(request, 'product.html', {
        'product': product,
        'other_products': other_products
    })


# View: Search
# The page for general searches
def search_view(request):
    data = search(request, None)

    return render(request, 'search.html', data)


# View: Order Summary
# The order summary page
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        data = {}

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            data['order'] = order
        except ObjectDoesNotExist:
            pass

        return render(self.request, 'order_summary.html', data)


# View: Checkout
# The checkout page
class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")


# View: Payment
# The payment page
class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)

        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }

            userprofile = self.request.user.userprofile

            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(userprofile.stripe_customer_id, limit=3, object='card')

                card_list = cards['data']

                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })

            return render(self.request, "payment.html", context)
        else:
            messages.warning(self.request, "You have not added a billing address")

            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = self.request.user.userprofile

        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(userprofile.stripe_customer_id)
                    customer.sources.create(source=token)
                else:
                    customer = stripe.Customer.create(email=self.request.user.email)
                    customer.sources.create(source=token)

                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:
                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(amount=amount, currency="usd", customer=userprofile.stripe_customer_id)
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(amount=amount, currency="usd", source=token)

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = userprofile.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order
                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                notifications.push(self.request.user, 'Order <span style = "font-family: Roboto-Medium;">#' + str(order.ref_code) + '</span> has been created and is waiting for a driver.', reverse('core:order', args = (order.ref_code,)))

                messages.success(self.request, "Your order was successful!")

                return redirect("/account/orders")

            except stripe.error.CardError as e:
                body = e.json_body

                err = body.get('error', {})

                messages.warning(self.request, f"{err.get('message')}")

                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")

                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)

                messages.warning(self.request, "Invalid parameters")

                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")

                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")

                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(self.request, "Something went wrong. You were not charged. Please try again.")

                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(self.request, "A serious error occurred. We have been notifed.")

                print(e)

                return redirect("/")

        messages.warning(self.request, "Invalid data received")

        return redirect("/payment/stripe/")


# View: Add to Cart
# The function to add a product to your cart
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        order_item = order.get_items(order).filter(item__slug=item.slug)

        if order_item.exists():
            order_item = order_item[0]

            order_item.quantity += 1
            order_item.save()

            messages.info(request, "This item quantity was updated.")

            return redirect("core:order-summary")
        else:
            order_item = OrderItem(item=item, order=order)
            order_item.save()

            messages.info(request, "This item was added to your cart.")

            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()

        order = Order.objects.create(user=request.user, ordered_date=ordered_date)

        order_item = OrderItem(item=item, order=order)
        order_item.save()

        messages.info(request, "This item was added to your cart.")

        return redirect("core:order-summary")


# View: Remove from Cart
# The function to remove a product from your cart
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.get_items(order).filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, order=order, order__ordered=False)[0]
            order_item.delete()

            messages.info(request, "This item was removed from your cart.")

            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")

            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")

        return redirect("core:product", slug=slug)


# View: Remove Single Item from Cart
# The function to remove a single product from your cart
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.get_items(order).filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, order=order, order__ordered=False)[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()

            messages.info(request, "This item quantity was updated.")

            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")

            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")

        return redirect("core:product", slug=slug)


# View: Get Coupon
# The function to process a coupon code
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


# View: Add Coupon
# The function to add a coupon to your order
class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')

                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()

                messages.success(self.request, "Successfully added coupon")

                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")

                return redirect("core:checkout")


# View: Request Refund
# The view to request a refund
class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")


# View: Order
# The page to show details about an order
class OrderView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(ref_code = kwargs['ref_code'])
            context={
                'object': order,
                'items': order.get_items(order)
            }
        except ObjectDoesNotExist:
            pass
        test = Order.objects.get(ref_code = kwargs['ref_code'])
        print(test.get_items(test))
        return render(self.request, 'driver_summary.html', context)


# View: Set Driver
# The function to attach a driver to an order
def set_driver(request, ref_code):
    order = Order.objects.get(ref_code = ref_code)
    print(order)
    order.driver = request.user.userprofile
    order.being_delivered = True
    order.save()

    notifications.push(order.user,
                       'Order <span style = "font-family: Roboto-Medium;">#' + str(order.ref_code) + '</span> has been assigned a driver. Watch for your delivery!',
                       reverse('core:order', args=(order.ref_code,)))

    return  HttpResponseRedirect('/db/driver/current')


# View: Set Delivered
# The function to set an order as delivered
def set_delivered(request, ref_code):
    order = Order.objects.get(ref_code = ref_code)
    order.being_delivered = False
    order.delivered = True
    order.delivered_date = timezone.now()
    order.save()

    notifications.push(order.user,
                       'Order <span style = "font-family: Roboto-Medium;">#' + str(order.ref_code) + '</span> has been delivered!',
                       reverse('core:order', args=(order.ref_code,)))

    return  HttpResponseRedirect('/db/driver/completed')


# View: Account
# The homepage for your account settings
@login_required
def account(request):
    data = {}

    if request.method == 'POST':
        form = EditUserForm(request.POST)

        if form.is_valid():
            request.user.userprofile.first_name = form.cleaned_data['first_name']
            request.user.userprofile.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']

            request.user.save()
            request.user.userprofile.save()
        else:
            print(form.errors)

        return redirect('core:account')

    if request.user.userprofile.vendor_owner:
        data['vendor'] = get_vendors(request.user.userprofile)

    return render(request, 'account.html', data)


# View: Account Page
# The view for each tab in the account page
@login_required
def account_page(request, page):
    try:
        data = {}

        profile = request.user.userprofile

        template = 'account/settings/' + page + '.html'

        if page == 'password':
            if request.method == 'POST':
                form = ChangePasswordForm(request.POST)

                if form.is_valid():
                    print('trying to change password')
                    print('password changed')
                else:
                    print(form.errors)

                return redirect('core:account')
        elif page == 'orders':
            orders = Order.objects.filter(user = request.user, ordered = True)

            data['orders'] = orders
        elif page == 'deliveries':
            orders = Order.objects.filter(driver = request.user.id, ordered = True, being_delivered = True, delivered = False)

            data['orders'] = orders

        if profile.vendor_owner:
            data['vendor'] = get_vendors(profile)

        return render(request, template, data)
    except:
        return redirect('core:account')


# View: Change Password
# The view to change your password
class ChangePassView(PasswordChangeView):
    success_url = reverse_lazy('core:account')


change_password = login_required(ChangePassView.as_view())


# The page that shows when youre not logged in; asks the user for their zip code for better results
def landing(request):
    return render(request, "landing.html")


# View: Read Notifications
# The function to read all of a users notifications
def read_notifications(request):
    response = {}

    if request.user.is_authenticated:
        notis = Notification.objects.filter(user = request.user.userprofile, read = False)

        for noti in notis:
            noti.read = True
            noti.save()

        response['success'] = True
    else:
        response['success'] = False

    return JsonResponse(response)


# View: Clear Notifications
# The function to clear all of a users notifications
def clear_notifications(request):
    response = {}

    if request.user.is_authenticated:
        notis = Notification.objects.filter(user = request.user.userprofile).delete()

        response['success'] = True
    else:
        response['success'] = True

    return JsonResponse(response)


# FUNCTIONS


# Function: Search
# The generic search function for any page to use
def search(request, optional_qs):
    data = {}

    query = ''
    price = None
    price_floor = 0
    price_ceiling = 9999999
    tags = []

    if request.method == 'GET':
        # Get every parameter passed from the request

        if 'q' in request.GET:
            query = request.GET['q']

        if 't' in request.GET:
            tags = request.GET.getlist('t')

        if 'p' in request.GET:
            price = request.GET['p']

            if '-' in price:
                parts = price.replace('$', '').split('-')

                price_floor = float(parts[0])
                price_ceiling = float(parts[1])

        '''print('QUERY: ' + query)
        print('TAGS: ' + str(tags))
        print('PRICE: ' + str(price))
        print('PRICE FLOOR: ' + str(price_floor))
        print('PRICE FLOOR: ' + str(price_ceiling))'''

        product_results, vendor_results = get_search_items(query, tags, price_floor, price_ceiling, None)

    if optional_qs:
        product_results, vendor_results = get_search_items(query, tags, price_floor, price_ceiling, optional_qs)

    data['query'] = query
    data['price'] = price
    data['all_tags'] = Tag.objects.all()
    data['selected_tags'] = tags

    data['product_results'] = product_results[:load_amount]
    data['vendor_results'] = vendor_results[:load_amount]

    print(query)

    return data


# Function: Get Search Items
# The generic function to get search items from a set of variables
def get_search_items(query, tags, price_floor, price_ceiling, optional_qs):
    # Creates select statements that can be dynamically used

    q_query = Q(title__contains = query)
    q_price = Q(price__range = (price_floor, price_ceiling))

    qs_products = None
    qs_vendors = None

    # Only searches products if tags are a parameter

    if tags:
        q_tags = Q(tags__name__in=tags)

        qs_products = Q(q_query & q_tags & q_price)
        qs_vendors = Q(q_query) # TODO: fix this
    else:
        qs_products = Q(q_query & q_price)
        qs_vendors = Q(q_query)

    # Adds optional queries ie. filtering a vendor page

    if optional_qs:
        for q in optional_qs:
            qs_products = Q(qs_products & q)

    product_results = Item.objects.filter(qs_products)
    vendor_results = Vendor.objects.filter(qs_vendors)

    return product_results, vendor_results


# Function: Serialize Items
# The function to turn search QuerySets into JSON friendly objects
def serialize_items(product_results, vendor_results):
    product_json = []
    vendor_json = []

    for item in product_results:
        product_json.append({
            'url': item.get_absolute_url(),
            'image_url': item.image.url,
            'title': item.title,
            'vendor': {
                'title': item.vendor.title,
                'vendor_url': item.vendor.get_absolute_url(),
            },
            'price': item.price,
            'tags': list(item.tags.all().values_list('name', 'color'))
        })

    return product_json, vendor_json


# Function: Search More
# A helper function for when a user loads more products on the search page
def search_more(request):
    data = {}

    start_index = request.session['start_index']

    print(start_index)

    query = request.session['query']
    tags = request.session['tags']

    product_results, vendor_results = get_search_items(query, tags)

    data['show_load_button'] = len(product_results) - start_index > load_amount

    request.session['start_index'] += load_amount

    product_json, vendor_json = serialize_items(product_results[start_index:start_index + load_amount], vendor_results[start_index:start_index + load_amount])

    data['product_results'] = product_json,
    data['vendor_results'] = vendor_json

    return JsonResponse(data)


# Function: Get Tags
# The function to get every tag that a vendor uses
def get_tags(vendor):
    items = Item.objects.filter(vendor = vendor)

    tags = []

    for item in items:
        print(item.tags.all())

        for tag in item.tags.all():
            if tag not in tags:
                tags.append(tag)

    return tags


# Function: Create Reference Code
# The function to create a reference code for an order
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


# Function: Is Valid Form
# Cant you just use form.is_valid() ?
def is_valid_form(values):
    valid = True

    for field in values:
        if field == '':
            valid = False

    return valid


# Function: Get Vendors
# The function to get every vendor that a user owns
#
# * Doesnt support multiple vendors
def get_vendors(owner):
    return Vendor.objects.get(owner = owner)
