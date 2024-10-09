from django.db import models
from Product.models import Product
from authentication.models import Order
# Create your models here.
from django.dispatch import receiver
from django.db.models.signals import post_save
from DDHotel import settings
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email =models.EmailField()
    phone = models.CharField(max_length=13)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add =True,null=True,blank=True)

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = "Contact Us "  # Singular name for the model
        verbose_name_plural = "Contact Us "
    
class Career(models.Model):
    name = models.CharField(max_length=50)
    email =models.EmailField()
    phone = models.CharField(max_length=13)
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add =True,null=True,blank=True)

    def __str__(self):
        return self.email
    

class Reservation(models.Model):
    name = models.CharField(max_length=50)
    email =models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=13,null=True,blank=True)
    no_persons = models.CharField(max_length=15,null=True,blank=True)
    date  =models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    status=(
        ('Pending','Pending'),
        ('Accepted','Accepted')
    )
    confirmation = models.CharField(max_length=15,choices=status,default='Pending')
    created_at = models.DateTimeField(auto_now_add =True,null=True,blank=True)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Check if the status is 'accepted'
        if self.confirmation == 'Accepted':
            # Call the send_email_reservation function
            send_email_reservation(self)

        # Save the Review object
        super().save(*args, **kwargs)
    
class Review(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    email =models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=13,null=True,blank=True)

    file = models.FileField(upload_to='Review-files/',null=True,blank=True)
    rating = models.IntegerField(default=0)
    item = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    message = models.TextField()
    
    created_at = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.name
    
    
        
        
def send_email_reservation(reservation):
    # Your existing email sending logic...
    EMAIL_HOST_USER = settings.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
    EMAIL_HOST = settings.EMAIL_HOST
    EMAIL_PORT = settings.EMAIL_PORT


    email_backend = EmailBackend(
        host=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
        use_tls=True,
    )
    
    html_content = render_to_string('Emails/reservation_confirm.html', {
        'name': reservation.name,
        'email': reservation.email,
        'phone': reservation.phone,
        'no_persons': reservation.no_persons,
        'date': reservation.date,
        'time': reservation.time,
        'confirmation': reservation.confirmation,
    })

    subject = "Reservation Confirmed."

    recipients = [f'{reservation.email}']
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=EMAIL_HOST_USER,
        to=recipients,
        connection=email_backend,
    )
    email.content_subtype = "html"
    email.send()
    
# Connect the post_save signal to the Review model
@receiver(post_save, sender=Reservation)
def reservation_save(sender, instance, **kwargs):
    # Check if the status is 'accepted'
    if instance.status == 'accepted':
        # Call the send_email_reservation function
        send_email_reservation(instance)