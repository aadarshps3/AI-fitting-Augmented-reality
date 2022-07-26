from django.contrib import admin

# Register your models here.
from app import models


admin.site.register(models.Customer)
admin.site.register(models.product)
admin.site.register(models.OrderItem)

