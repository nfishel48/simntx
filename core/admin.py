from django.contrib import admin
from .models import Item, OrderItem, Order, Vendor, UserProfile, Post, Tag, Notification, Address, UserAddress, VendorHours, PostComment, PostLink, PostImage

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Vendor)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Notification)
admin.site.register(Address)
admin.site.register(UserAddress)
admin.site.register(VendorHours)
admin.site.register(PostComment)
admin.site.register(PostLink)
admin.site.register(PostImage)