from django.db import models


class Vendor(models.Model):
    name = models.TextField(default='NAN', max_length=50)
    phone_num = models.TextField(default='0', max_length=11)
    address = models.TextField(default='311 Ballard Street')
    vid = models.IntegerField()
