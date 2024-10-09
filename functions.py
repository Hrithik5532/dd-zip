import os
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from DDHotel import settings
from django.template.loader import render_to_string

def send_email_otp( user, otp):
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
    subject = "DDHotels One Time Password (OTP)"
    body = """
    
    <!DOCTYPE html>
<html lang="en">


<div style="margin: 20px auto;
text-align: center; margin: 0 auto; width: 650px; font-family: 'Public Sans', sans-serif; background-color: #e2e2e2; display: block;">
    <table align="center" border="0" cellpadding="0" cellspacing="0"
        style="background-color: white; width: 100%; box-shadow: 0px 0px 14px -4px rgba(0, 0, 0, 0.2705882353);-webkit-box-shadow: 0px 0px 14px -4px rgba(0, 0, 0, 0.2705882353);">
        <tbody>
            <tr>
                <td>
                    <table class="header-table" align="center" border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr class="header"
                                    style="background-color: #f7f7f7;display: flex;align-items: center;width: 100%;    justify-content: center !important;">
                                    <td class="header-logo" style="padding: 10px 32px;">
                                        <a href="https://bombay2goa.co.uk" style="display: block; text-align: left;">
                                            <img src="https://bombay2goa.co.uk/statics/images/B2G-1.png" style="width:8rem" class="main-logo" alt="logo">
                                        </a>
                                    </td>
                                </tr>
                            </table>

                    <table class="contant-table" style="margin-top: 40px;" align="center" border="0" cellpadding="0"
                        cellspacing="0" width="100%">
                        <thead>
                            <tr style="display: block;">
                                <td style="display: block;">
                                    <h3
                                        style="font-weight: 700; font-size: 20px; margin: 0; text-transform: uppercase;">
                                        Hi {first_name} And Welcome To DDHotels!</h3>
                                </td>

                            </tr>
                        </thead>
                    </table>

                    <table class="button-table" style="margin: 34px 0;" align="center" border="0" cellpadding="0"
                        cellspacing="0" width="100%">
                        <thead>
                            <tr style="display: block;">
                                <td style="display: block;">
                                    <span style="padding: 9px;font-size: 25px;font-weight: 600;">{otp} </span>
                                </td>
                            </tr>
                        </thead>
                    </table>

                    <table class="contant-table" align="center" border="0" cellpadding="0" cellspacing="0" width="100%">
                        <thead>
                            <tr style="display: block;">
                                <td style="display: block;">
                           
                                </td>
                            </tr>
                        </thead>
                    </table>

                    <table class="text-center footer-table" align="center" border="0" cellpadding="0" cellspacing="0"
                        width="100%"
                        style="background-color: #282834; color: white; padding: 24px; overflow: hidden; z-index: 0; margin-top: 30px;">
                        <tr>
                            <td>
                                <table border="0" cellpadding="0" cellspacing="0" class="footer-social-icon text-center"
                                    align="center" style="margin: 8px auto 11px;">
                                    <tr>
                                        <td>
                                            <h4 style="font-size: 19px; font-weight: 700; margin: 0;"> <span
                                                    class="theme-color">Bombay2Goa</span></h4>
                                        </td>
                                    </tr>
                                </table>
                               
                                
                                
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </tbody>
    </table>
</div>

</html>
    """.format(first_name=user.first_name,otp=otp)
    recipients = [user.email]

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=EMAIL_HOST_USER,
        to=recipients,
        connection=email_backend,
    )
    email.content_subtype = "html"
    email.send()





def send_email_reset_link( user, link,user_email):
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_PORT = os.environ.get("EMAIL_PORT")

    email_backend = EmailBackend(
        host=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
        use_tls=True,
    )
    subject = "Zebahomes One Time Password (OTP)"
    body = """
    
    <!DOCTYPE html>
<html lang="en">


<div style="margin: 20px auto;
text-align: center; margin: 0 auto; width: 650px; font-family: 'Public Sans', sans-serif; background-color: #e2e2e2; display: block;
        
">
    <table align="center" border="0" cellpadding="0" cellspacing="0"
        style="background-color: white; width: 100%; box-shadow: 0px 0px 14px -4px rgba(0, 0, 0, 0.2705882353);-webkit-box-shadow: 0px 0px 14px -4px rgba(0, 0, 0, 0.2705882353);">
        <tbody>
            <tr>
                <td>
                    <table class="header-table" align="center" border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr class="header"
                            style="background-color: #f7f7f7;display: flex;align-items: center;justify-content: space-between;width: 100%;">
                            <td class="header-logo" style="padding: 10px 32px;">
                                <a href="../front-end/index.html" style="display: block; text-align: left;">
                                    <img src="https://bombay2goa.co.uk/static/assets/images/logo/logo_5.png" class="main-logo" alt="logo">
                                </a>
                            </td>
                        </tr>
                    </table>

                    <table class="contant-table" style="margin-bottom: -6px;" align="center" border="0" cellpadding="0"
                        cellspacing="0" width="100%">
                        <thead>
                            <tr>
                                <td>
                                    <img src="https://themes.himani'cc.com.com/fastkart/email-templete/images/welcome-poster.jpg" alt="">
                                </td>
                            </tr>
                        </thead>
                    </table>

                    <table class="contant-table" style="margin-top: 40px;" align="center" border="0" cellpadding="0"
                        cellspacing="0" width="100%">
                        <thead>
                            <tr style="display: block;">
                                <td style="display: block;">
                                    <h3
                                        style="font-weight: 700; font-size: 20px; margin: 0; text-transform: uppercase;">
                                        Hi {first_name} And Welcome To Zebahomes!</h3>
                                </td>

                                <td>
                                    <p
                                        style="font-size: 14px;font-weight: 600;width: 82%;margin: 8px auto 0;line-height: 1.5;color: #939393;font-family: 'Nunito Sans', sans-serif;">
                                        We hope our product will lead you, like many other before you. to a place where
                                        yourideas where your ideas can spark and grow.n a place where you’ll find all
                                        your inspiration needs. before we get started, we’ll need to verify your email.
                                    </p>
                                </td>
                            </tr>
                        </thead>
                    </table>

                    <table class="button-table" style="margin: 34px 0;" align="center" border="0" cellpadding="0"
                        cellspacing="0" width="100%">
                        <thead>
                            <tr style="display: block;">
                                <td style="display: block;">
                                    <a href="{link}" class="password-button">{link}</button>
                                </td>
                            </tr>
                        </thead>
                    </table>

                    <table class="contant-table" align="center" border="0" cellpadding="0" cellspacing="0" width="100%">
                        <thead>
                            <tr style="display: block;">
                                <td style="display: block;">
                                    <p
                                        style="font-size: 14px; font-weight: 600; width: 82%; margin: 0 auto; line-height: 1.5; color: #939393; font-family: 'Nunito Sans', sans-serif;">
                                        If you have any question, please email us at <span
                                            class="theme-color">Fastkart@example.com</span> or vixit our <span
                                            class="theme-color">FAQs.</span> You can also chat with a real live human
                                        during our operating hours. they can answer questions about account or help you
                                        with your meditation practice.</p>
                                </td>
                            </tr>
                        </thead>
                    </table>

                    <table class="text-center footer-table" align="center" border="0" cellpadding="0" cellspacing="0"
                        width="100%"
                        style="background-color: #282834; color: white; padding: 24px; overflow: hidden; z-index: 0; margin-top: 30px;">
                        <tr>
                            <td>
                                <table border="0" cellpadding="0" cellspacing="0" class="footer-social-icon text-center"
                                    align="center" style="margin: 8px auto 11px;">
                                    <tr>
                                        <td>
                                            <h4 style="font-size: 19px; font-weight: 700; margin: 0;">Shop For <span
                                                    class="theme-color">Fastkart</span></h4>
                                        </td>
                                    </tr>
                                </table>
                               
                                
                                
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </tbody>
    </table>
</div>

</html>
    """.format(first_name=user.first_name,link=link)
    recipients = [user_email]

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=EMAIL_HOST_USER,
        to=recipients,
        connection=email_backend,
    )
    email.content_subtype = "html"
    email.send(fail_silently=False,
)



def send_email_order_confirm(request,user,order,status):
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
    if status=='success':
        
        html_content = render_to_string('Emails/order_success.html', {
            'name': order.customer_first_name,
            'email': order.customer_email,
            'order_id':order.id,
            'date':order.updated_at,
            'status':status
            
            
        })
    else:
        html_content = render_to_string('Emails/order_fail.html', {
            'name': str(order.customer_first_name) + str(order.customer_last_name),
            'email': str(order.customer_email),
            'order_id':order.id,
            'date':order.created_at,
            'status':status
            
            
        })

    subject = "Order Details"

    recipients = [f'{order.customer_email}']
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=EMAIL_HOST_USER,
        to=recipients,
        connection=email_backend,
    )
    email.content_subtype = "html"
    email.send()
    
    
    
    
    subject = "New order Created"
    body = """ 
        New Reservation Request is generated ...!! \n
        Name : {name}\n
        Email : {email}\n
        Order Id : {id}\n
        Date : {date}\n
        <a href="https://bombay2goa.co.uk/admin/authentication/order/{id}/change/" target="_blank">View On Admin Panel</a>
    """.format(name=str(order.customer_first_name) + str(order.customer_last_name),email=order.customer_email,date=order.created_at,id=order.id)
    recipients = ['bombay2goa.hotel@gmail.com']
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=EMAIL_HOST_USER,
        to=recipients,
        connection=email_backend,
    )
    email.content_subtype = "html"
    email.send()
    

def send_email_contact(request,email,name,time):
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
    subject = "New Contact Enquiry !!"
    body = """ 
        New Enquiry is generated ...!! \n
        Name : {name}\n
        Email : {email}\n
        Created at : {time}
    """.format(name=name,email=email,time=time)
    recipients = [EMAIL_HOST]
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=EMAIL_HOST_USER,
        to=recipients,
        connection=email_backend,
    )
    email.content_subtype = "html"
    email.send()

    
    

def send_email_reservation(request,reservation):
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
    
    html_content = render_to_string('Emails/reservation_email_template.html', {
        'name': reservation.name,
        'email': reservation.email,
        'phone': reservation.phone,
        'no_persons': reservation.no_persons,
        'date': reservation.date,
        'time': reservation.time,
        'confirmation': reservation.confirmation,
    })

    subject = "Reservation Request Submitted Successfully."

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
    
    
    
    
    subject = "New Reservation Request"
    body = """ 
        New Reservation Request is generated ...!! \n
        Name : {name}\n
        Email : {email}\n
        No. of Persons : {no_persons}\n
        Date : {date}\n
        Time : {time}\n
        Confirmation : {confirmation}
        <a href="https://bombay2goa.co.uk/admin/Reservations_Reviews_Contact/reservation/{id}/change/" target="_blank">View On Admin Panel</a>
    """.format(name=reservation.name,email=reservation.email,date=reservation.date,id=reservation.id,time=reservation.time,no_persons=reservation.no_persons,confirmation=reservation.confirmation)
    recipients = ['bombay2goa.hotel@gmail.com']
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=EMAIL_HOST_USER,
        to=recipients,
        connection=email_backend,
    )
    email.content_subtype = "html"
    email.send()
    
    





def send_email_reservation(request,reservation):
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
    
    
    

    
    



def send_email_newsletter(request):
    pass