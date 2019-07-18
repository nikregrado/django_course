from django.contrib import admin

from .models import Category, Publisher, Game, Order, Cart, Key

# Register your models here.

admin.site.register(Category)
admin.site.register(Publisher)
admin.site.register(Game)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Key)
