from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import profile,Show,tickettype,comment,showtype
admin.site.register(profile)
admin.site.register(Show)
admin.site.register(tickettype)
admin.site.register(comment)
admin.site.register(showtype)
