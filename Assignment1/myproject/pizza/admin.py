from django.contrib import admin
from .models import Pizza, Size, Crust, Sauce, Cheese

admin.site.register(Pizza)
admin.site.register(Size)
admin.site.register(Crust)
admin.site.register(Sauce)
admin.site.register(Cheese)