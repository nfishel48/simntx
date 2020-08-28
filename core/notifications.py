from django.urls import reverse

from core.models import Notification


def push(user, text, link):
    notification = Notification(user = user.userprofile, text = text, link = link)

    notification.save()


def order_created(user, ref_code):
    push(user, 'Order <span style = "font-family: Roboto-Medium;">#' + str(ref_code) + '</span> has been created and is waiting to be approved by the vendor.', reverse('core:order', args = (ref_code,)))


def order_approved_denied(user, ref_code, approved):
    push(user, 'Order <span style = "font-family: Roboto-Medium;">#' + str(
                               ref_code) + '</span> has been ' + ('approved by the vendor and is waiting for a driver. Your card has been charged.' if approved else 'denied by the vendor.'), reverse('core:order', args = (ref_code,)))


def order_assigned_unassigned(user, ref_code, assigned):
    push(user, 'Order <span style = "font-family: Roboto-Medium;">#' + str(ref_code) + '</span> has been ' + ('assigned a driver. Watch for your delivery!' if assigned else 'unassigned its driver. Its now waiting for another.'), reverse('core:order', args = (ref_code,)))


def order_cancelled(user, ref_code, message):
    push(user, 'Order <span style = "font-family: Roboto-Medium;">#' + str(
                                   ref_code) + '</span> has been cancelled. <span style "color: var(--light-red)">' + message + '</span>', reverse('core:order', args = (ref_code,)))


def order_delivered(user, ref_code):
    push(user, 'Order <span style = "font-family: Roboto-Medium;">#' + str(
                                   ref_code) + '</span> has been delivered!', reverse('core:order', args = (ref_code,)))