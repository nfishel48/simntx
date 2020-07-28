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

from allauth.account.views import PasswordChangeView
from allauth.account.forms import ChangePasswordForm

from .forms import *
from .models import *
from .templatetags.tags import get_normal_time

from . import notifications

import random
import string
import stripe
import arrow
import math

from random import shuffle

stripe.api_key = settings.STRIPE_SECRET_KEY

search_load_amount = 15
store_sponsors_limit = 5

# View: Index
# The view that redirects to the front page
def index(request):
    return redirect('/feed')

# View: Feed
# The page for posts from vendors you follow
def feed(request):
    if request.user.is_authenticated == True:
        posts = Post.objects.filter(vendor__in = request.user.userprofile.following.all()).order_by('-posted')

        #messages.info(request, 'Info message');
        #messages.success(request, 'Success message');
        #messages.warning(request, 'Warning message');
        #messages.error(request, 'Error message');

        return render(request, 'feed.html', {
            'posts': posts,
        })
    else:
        return redirect("core:landing")


# View: Store
# The store showing all vendors and products
def store(request):
    if request.user.is_authenticated == True:
        vendors = Vendor.objects.all()[:10]
        products = Item.objects.all()[:10]
        food = Item.objects.filter(general_tags = GeneralTag.objects.get(name ='food'))[:10]

        store_sponsors = get_store_sponsors()

        general_tags = GeneralTag.objects.all()

        for vendor in vendors:
            vendor.general_tags = get_general_tags(vendor.id)

        return render(request, 'store.html', {
            'vendors': vendors,
            'products': products,
            'food': food,
            'general_tags': general_tags,
            'store_sponsors': store_sponsors,
        })
    else:
       return render(request, 'landing.html')


# View: Store
# This method is a overloaded version of the previous, this is called by the landing page
def store_landing(request, context):
    if request.user.is_authenticated == True:
        vendors = Vendor.objects.all()[:10]
        products = Item.objects.all()[:10]
        food = Item.objects.filter(general_tags = GeneralTag.objects.get(name ='food'))[:10]

        general_tags = GeneralTag.objects.all()

        for vendor in vendors:
            vendor.general_tags = get_general_tags(vendor.id)

        return render(request, 'store.html', {
            'vendors': vendors,
            'products': products,
            'food': food,
            'general_tags': general_tags,
            })
    else:
        zip_code = request.POST.get('zip_code')
        vendors = Vendor.objects.filter(address__zip = zip_code)[:10]
        # products = Item.objects.all()[:10]
        # food = Item.objects.filter(general_tags = GeneralTag.objects.get(name ='food'))[:10]

        general_tags = GeneralTag.objects.all()

        for vendor in vendors:
            vendor.general_tags = get_general_tags(vendor.id)

        return render(request, 'store.html', {
            'vendors': vendors,
            # 'products': products,
            # 'food': food,
            'general_tags': general_tags,
            })



# View: Vendor
# The page for a specific vendor
def vendor(request, slug):
    return redirect('core:vendor_store', slug=slug)


# View: Vendor Feed
# The tab on a vendors page that shows all of their posts
def vendor_feed(request, slug):
    vendor = Vendor.objects.get(slug=slug)

    posts = Post.objects.filter(vendor = vendor)

    return render(request, 'vendor_feed.html', {
        'vendor': vendor,
        'posts': posts,
    })


# View: Vendor Store
# The store showing all the vendors products
def vendor_store(request, slug):
    vendor = Vendor.objects.get(slug=slug)
    products = Item.objects.filter(vendor=vendor)

    vendor.general_tags = get_general_tags(vendor.id)

    data = search(request, [Q(vendor=vendor)])  # Only searches items from this vendor

    data['vendor'] = vendor
    data['products'] = products

    return render(request, 'vendor_store.html', data)


# View: Vendor About
# The page showing all relevent information about a vendor
def vendor_about(request, slug):
    data = {}

    vendor = Vendor.objects.get(slug=slug)

    data['vendor'] = vendor

    return render(request, 'vendor_about.html', data)


# View: Product
# The page for a specific product
def product(request, slug):
    product = Item.objects.get(slug = slug)
    other_products = Item.objects.filter(vendor = product.vendor)

    return render(request, 'product.html', {
        'product': product,
        'other_products': other_products
    })


def post(request, id):
    data = {}

    post = Post.objects.filter(id = id)

    if post.exists():
        post = post[0]

        data['post'] = post
    else:
        return redirect('core:feed')

    return render(request, 'post.html', data)


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
            context = {
                'order': order
            }
        except ObjectDoesNotExist:
            pass

        return render(self.request, 'order_summary.html', context)


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

            shipping_address_qs = UserAddress.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = UserAddress.objects.filter(
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
                use_default_shipping = form.cleaned_data.get('use_default_shipping')

                if use_default_shipping:
                    print("Using the defualt shipping address")

                    address_qs = UserAddress.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )

                    if address_qs.exists():
                        shipping_address = address_qs[0]

                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, "No default shipping address available")

                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")

                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = UserAddress(
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

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')

                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')

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
                    address_qs = UserAddress.objects.filter(
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

                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = UserAddress(
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

                        set_default_billing = form.cleaned_data.get('set_default_billing')

                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.info(self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid payment option selected")

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
    item = Item.objects.filter(slug = slug)

    if item.exists():
        item = item[0]
    else:
        messages.error(request, 'This item does not exist.')

        return redirect('core:store')

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    #if order exists 
    if order_qs.exists():

        order = order_qs[0]
        
        #if the item being added is from the same vendor
        if item.vendor == order.vendor:
            
            order_item = order.get_items(order).filter(item__slug=item.slug)

            if order_item.exists():
                order_item = order_item[0]

                order_item.quantity += 1
                order_item.save()

                messages.info(request, "This item quantity was updated.")

                return redirect("core:order-summary")
            else:
                order_item = OrderItem(item=item, order=order, in_stock = True)
                order_item.save()

                messages.info(request, "This item was added to your cart.")

                return redirect("core:order-summary")
            
        else:
            messages.info(request, "Plese finish your order from the previous vendor before you order from a second")
            dir(item.vendor)

            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()

        print("\n\nITEM: " + str(item))
        print("\n\nVENDOR: " + str(item.vendor))
        print("\n\nUSER: " + str(request.user.userprofile))

        #create new order marked for vendor of inintial Item
        order = Order(user=request.user, ordered_date=ordered_date, vendor = item.vendor)

        print('\n\n\n' + str(order.vendor) + '\n\n\n')

        order.save()

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
            #if order is empty
            if order.get_items(order).filter().exists():
                print('I do nothing')
            else:
                order.delete()

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
                 #if order is empty
                if order.get_items(order).filter().exists():
                    print('I do nothing')
                else:
                    order.delete()

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
    except:
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
            except:
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
        data = {}

        try:
            order = Order.objects.get(ref_code = kwargs['ref_code'])

            data = {
                'order': order,
                'items': order.get_items(order)
            }
        except ObjectDoesNotExist:
            pass

        return render(self.request, 'order.html', data)


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


# View: Account
# The homepage for your account settings
@login_required
def account(request):
    data = {}

    if request.method == 'POST':
        form = EditUserForm(request.POST)

        if form.is_valid():
            user = form.save(request)

            print(user)
        else:
            print(form.errors)

        return redirect('core:account')

    if request.user.userprofile.vendor_owner == True:
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


# View: Landing
# The page that shows when youre not logged in; asks the user for their zip code for better results
def landing(request):
    if request.method == 'POST':

        form = ZipForm(request.POST)

        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']
            context ={
                zip_code: 'zip_code'
            }
            return store_landing(request, context)
    
    form = ZipForm()
    return render(request, "landing.html", {'form': form})


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
@login_required
def clear_notifications(request):
    response = {}

    if request.user.is_authenticated:
        notis = Notification.objects.filter(user = request.user.userprofile).delete()

        response['success'] = True
    else:
        response['success'] = True

    return JsonResponse(response)

@login_required
def follow_action(request, slug):
    data = {}

    vendor = Vendor.objects.filter(slug = slug)

    if vendor.exists():
        if request.user.userprofile.following.filter(slug = slug).exists():
            request.user.userprofile.following.remove(vendor[0])
        else:
            request.user.userprofile.following.add(vendor[0])

        print('FOLLOWING: ' + str(request.user.userprofile.following.filter(slug = slug).exists()))

        data['success'] = True
    else:
        data['success'] = False

    return JsonResponse(data)

@login_required
def like_action(request, id):
    data = {}

    post = Post.objects.filter(id = id)

    if post.exists():
        post = post[0]

        if post in request.user.userprofile.liked_posts.all():
            request.user.userprofile.liked_posts.remove(post)

            data['following'] = False
        else:
            request.user.userprofile.liked_posts.add(post)

            data['following'] = True

        data['success'] = True
    else:
        data['success'] = False

    return JsonResponse(data)

@login_required
def comment(request):
    data = {
        'success': False,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name
    }

    if 'post_id' in request.GET and 'text' in request.GET:
        post = Post.objects.filter(id = int(request.GET['post_id']))

        print(post)

        if post.exists():
            post = post[0]

            comment = PostComment(post = post, text = request.GET['text'], user = request.user)
            comment.save()

            print(comment)

            data['success'] = True
        else:
            print('Post does not exist')
    else:
        print(request.GET)

    return JsonResponse(data)

@login_required
def comments(request):
    data = {}

    amount = 10

    if 'post_id' in request.GET and 'index' in request.GET:
        post = Post.objects.filter(id=int(request.GET['post_id']))

        print('POST:' + str(post))

        if post.exists():
            post = post[0]

            index = int(request.GET['index'])

            q_comments = PostComment.objects.filter(post = post).order_by('-posted')[index * amount + 1:(index * amount) + amount + 1]

            comments = []

            for comment in q_comments:
                new_comment = {
                    'text': comment.text,
                    'first_name': comment.user.first_name,
                    'last_name': comment.user.last_name,
                    'posted': get_normal_time(comment.posted)
                }

                comments.append(new_comment)

            data['comments'] = comments
            data['more_to_load'] = len(comments) == 10
        else:
            print('Post does not exist')
    else:
        print('GET: ' + str(request.GET))

    return JsonResponse(data)

# FUNCTIONS


# Function: Search
# The generic search function for any page to use
def search(request, optional_qs):
    data = {}

    query = ''
    price = None
    price_floor = 0
    price_ceiling = 9999999
    general_tags = []
    page = 1
    type = 'products'

    if request.method == 'GET':
        # Get every parameter passed from the request

        if 'q' in request.GET:
            query = request.GET['q']

        if 't' in request.GET:
            general_tags = request.GET.getlist('t')

        if 'p' in request.GET:
            price = request.GET['p']

            if '-' in price:
                parts = price.replace('$', '').split('-')

                price_floor = float(parts[0])
                price_ceiling = float(parts[1])

        if 'pg' in request.GET:
            page = int(request.GET['pg'])

        if 'tp' in request.GET:
            if request.GET['tp'] == 'vendors':
                type = 'vendors'

        product_results, vendor_results = get_search_items(query, general_tags, price_floor, price_ceiling, type, None)

    if optional_qs:
        product_results, vendor_results = get_search_items(query, general_tags, price_floor, price_ceiling, type, optional_qs)

    if type == 'vendors':
        results = vendor_results
    else:
        results = product_results

    total_pages = math.ceil(len(results) / search_load_amount)

    lower_bound = page - 4 if page - 4 > 0 else 1
    upper_bound = page + 4 if page + 4 <= total_pages else total_pages

    shown_lower = (page - 1) * search_load_amount
    shown_upper = page * search_load_amount

    data['query'] = query
    data['price'] = price
    data['page_num'] = page
    data['all_tags'] = GeneralTag.objects.all()
    data['selected_tags'] = general_tags
    data['type'] = type

    data['total_pages'] = total_pages
    data['bound'] = range(lower_bound, upper_bound + 1)
    data['shown_lower'] = shown_lower + (1 if len(results) > 0 else 0)
    data['shown_upper'] = shown_lower + len(results[shown_lower:shown_upper])
    data['total_results'] = len(results)

    data['results'] = results[shown_lower:shown_upper]

    return data


# Function: Get Search Items
# The generic function to get search items from a set of variables
def get_search_items(query, general_tags, price_floor, price_ceiling, type, optional_qs):
    # Creates select statements that can be dynamically used

    q_query = Q(title__icontains = query.lower())
    q_price = Q(price__range = (price_floor, price_ceiling))

    qs_products = None
    qs_vendors = None

    # Only searches products if tags are a parameter

    if general_tags:
        q_general_tags = Q(general_tags__name__in=general_tags)

        qs_products = Q(q_query & q_general_tags & q_price)
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

    product_results, vendor_results = highlight_promoted_items(product_results, vendor_results)

    return product_results, vendor_results


def highlight_promoted_items(product_results, vendor_results):
    product_results = list(product_results)
    promoted_items = list(ProductPromotion.objects.filter(product__in = product_results))

    shuffle(promoted_items)

    for item in promoted_items[:3]:
        product_results.remove(item.product)

        item.product.promotion = True

        product_results = [item.product] + product_results

    print(product_results)

    return product_results, vendor_results


# Function: Get Tags
# The function to get every tag that a vendor uses
def get_general_tags(vendor):
    items = Item.objects.filter(vendor = vendor)

    general_tags = []

    for item in items:
        print(item.general_tags.all())

        for tag in item.general_tags.all():
            if tag not in general_tags:
                general_tags.append(tag)

    return general_tags


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

#
# Function : approve delivery
# This function is used by vendors to aprove a delivery and 
# allow a driver too assigan the delivery
def approve_order(request, ref_code):
    order = Order.objects.filter(ref_code = ref_code)
    
    if order.exists() and not order[0].being_delivered:
        order = order[0]
        
        #for items in order
            #if orderitem is not authorized
                #order.autherized == false 
            #else
                #order.autherized == true
        order.authorized = True
        order.save()

        notifications.push(order.user,
                'Order <span style = "font-family: Roboto-Medium;">#' + str(order.ref_code) + '</span> has been approved by a vendor and will soon be assigned to a driver',
               reverse('core:order', args=(order.ref_code,)))

    return redirect('dashboards:vendor')


def get_store_sponsors():
    sponsors = list(StorePromotion.objects.all())

    shuffle(sponsors)

    return sponsors[:store_sponsors_limit]