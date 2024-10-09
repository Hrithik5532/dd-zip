from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'item', 'message', 'created_at')

    # readonly_fields = ('name', 'email', 'phone', 'file', 'rating', 'item', 'order', 'message', 'created_at')

    
class ContactAdmin(admin.ModelAdmin):
    
    list_display = ('name',  'email', 'phone', 'created_at')  # Fields to display in the admin list view

    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name',  'email', 'phone', 'date','confirmation')  # Fields to display in the admin list view

    readonly_fields = ('name', 'email', 'phone', 'date','no_persons','time' ,'message', 'created_at')

    

admin.site.register(Review,ReviewAdmin)
admin.site.register(ContactUs,ContactAdmin)


admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Career)