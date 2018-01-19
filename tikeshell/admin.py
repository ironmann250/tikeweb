from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Show,ShowAdmin)
admin.site.register(tickettype)
admin.site.register(comment)
admin.site.register(Keyword)
admin.site.register(Review)
admin.site.register(Picture)
admin.site.register(Account, AccountAdmin)
admin.site.register(SellerAccount)
admin.site.register(Category)
admin.site.register(Venue)
admin.site.register(Ticket,TicketAdmin)
