from django.contrib import admin
from .models import *

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Vendor)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(GeneralTag)
admin.site.register(Address)
admin.site.register(UserAddress)
admin.site.register(VendorHours)
admin.site.register(PostComment)
admin.site.register(PostLink)
admin.site.register(PostImage)
admin.site.register(StorePromotion)
admin.site.register(PostPromotion)
admin.site.register(ProductPromotion)