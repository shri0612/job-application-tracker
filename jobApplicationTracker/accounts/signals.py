from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings


# 🔔 Send login alert when user logs in
@receiver(user_logged_in)
def send_login_alert(sender, request, user, **kwargs):
    print('User check',user)
    # if not user.email:
    #     print("⚠️ No email set for:", user.username)
    #     return

    # display_name = user.username or user.email.split("@")[0]
    # subject = f"Welcome {display_name}, your login was successful 🎉"
    # print(user.username)

    try:
        user_email = user.email
        user_name = user.get_full_name() or user.username
        login_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        # Get user's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # Email subject
        subject = '🔐 Login Notification - Your Account Activity'

        # Plain text message
        message = f"""
        Hello {user_name},

        We detected a login to your account.

            Login Details:
            - Time: {login_time}
            - IP Address: {ip_address}
            - Device: {request.META.get('HTTP_USER_AGENT', 'Unknown')}

        If this was you, no action is needed. If you didn't login, please secure your account immediately.

        Best regards,
        The Bakery Team
        """

        # HTML message
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #4caf50; text-align: center;">🔐 Login Notification</h2>
                    <p>Hello <strong>{user_name}</strong>,</p>
                    <p>We detected a login to your account.</p>
                    
                    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #4caf50;">Login Details:</h3>
                        <p><strong>⏰ Time:</strong> {login_time}</p>
                        <p><strong>📍 IP Address:</strong> {ip_address}</p>
                    </div>
                    
                    <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
                        <p style="margin: 0;"><strong>⚠️ Security Notice:</strong></p>
                        <p style="margin: 5px 0 0 0;">If this wasn't you, please secure your account immediately by changing your password.</p>
                    </div>
                    
                    <p style="color: #777; font-size: 12px; text-align: center; margin-top: 30px;">
                        This is an automated security notification.<br>
                        Best regards,<br>
                        The Application tracker Team
                    </p>
                </div>
            </body>
        </html>
        """

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
            fail_silently=True,  # Don’t break login if email fails
        )
        print(f"✓ Login notification email sent to {user_email}")

    except Exception as e:
        print(f"✗ Error sending login email: {str(e)}")
 
 

    # # Plain text fallback
    # text_content = strip_tags(html_content)

    # email = EmailMultiAlternatives(
    #     subject,
    #     text_content,
    #     "shri2178499@gmail.com",   # FROM (must be verified in SES)
    #     [user.email],              # TO (must be verified in sandbox)
    # )
    # email.attach_alternative(html_content, "text/html")

    # try:
    #     email.send()
    #     print(f"✅ Login email sent to {user.email}")
    # except Exception as e:
    #     print("❌ Login alert email failed:", repr(e))


# 📧 Ensure all user emails are stored in lowercase
@receiver(pre_save, sender=User)
def lowercase_email(sender, instance, **kwargs):
    if instance.email:
        instance.email = instance.email.lower()
