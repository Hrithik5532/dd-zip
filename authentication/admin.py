from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Newsletter)
admin.site.register(GiftCard)
admin.site.unregister(Group)
admin.site.register(PurchasedGiftCard)
admin.site.register(GiftCardDesigns)
admin.site.register(DiscountCoupon)
# admin.site.register(Cart)

class OrderAdmin(admin.ModelAdmin):
    
    list_display = ('id','order_done', 'order_type' ,'payment_status' ,'created_at'  )
    search_fields = ('payment_status','id')
    fieldsets = (
        ('Order Items Details', {
            'fields': (
                'order_done',
                'order_type',
                'get_order_items_details',
            ),
            'classes': ('collapse',),  # Optional: Collapse the section by default
        }),
        ('Customer Information', {
            'fields': (
                'customer_first_name', 
                'customer_last_name', 
                'customer_email', 
                'customer_contact',
            ),
        }),
        ('Address Information', {
            'fields': (
                'address_line_1', 
                'address_line_2', 
                'city', 
                'state', 
                'postal_code',
            ),
        }),
        ('Payment Information', {
            'fields': (
                'payment_status', 
                'payment_id', 
                'payment_amount', 
                'sub_total', 
                'total', 
                'tax_percentage',
                'tax',
                'deliveryCharges',
            ),
        }),
        
    )
    readonly_fields = ('customer_first_name', 'tax_percentage','order_type',
                'tax','customer_last_name', 'customer_email', 'customer_contact', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'payment_status', 'payment_id', 'payment_amount', 'sub_total', 'total', 'deliveryCharges', 'get_order_items_details')

    def get_order_items_details(self, obj):
        """
        Custom method to display order items details in a readable format.
        """
        items_details = []
        for order_item in obj.order_items.all():
            items_details.append(f"Menu Item: {order_item.product.name}, \n Quantity: {order_item.quantity}")
        return '\n'.join(items_details)

    get_order_items_details.short_description = 'Order Items Details'

admin.site.register(Order,OrderAdmin)
# admin.site.register(OrderItem)
