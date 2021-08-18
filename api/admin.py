from django.contrib import admin
from users.models import *
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Command)
admin.site.register(Delivery)
admin.site.register(CommandRow)
admin.site.register(DeliveryDetails)
