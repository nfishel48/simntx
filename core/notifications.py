from core.models import Notification

def push(user, text, link):
    notification = Notification(user = user.userprofile, text = text, link = link)

    notification.save()