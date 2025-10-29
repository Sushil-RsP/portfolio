# Create your views here.

# contact/views.py

from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from .forms import ContactForm
from django.conf import settings
import os

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to database first (most important!)
            form.save()
            
            # Try to send email
            # NOTE: Gmail SMTP works ONLY locally, NOT on Render (port 587 blocked)
            # For Render, use SendGrid by adding SENDGRID_API_KEY environment variable
            try:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']

                # Check if SendGrid API key is configured (works on Render)
                sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
                
                if sendgrid_api_key:
                    # Use SendGrid API (works on Render free tier!)
                    from sendgrid import SendGridAPIClient
                    from sendgrid.helpers.mail import Mail, Personalization, Email as SGEmail
                    
                    # Create message with better spam score
                    mail_message = Mail()
                    mail_message.from_email = SGEmail('sushilchavan2468@gmail.com', 'Sushil Chavan Portfolio')
                    mail_message.subject = f'Portfolio Contact: {name}'  # Simpler subject, less spammy
                    mail_message.reply_to = SGEmail(email, name)
                    
                    # Add personalization
                    personalization = Personalization()
                    personalization.add_to(SGEmail('sushilchavan2468@gmail.com'))
                    mail_message.add_personalization(personalization)
                    
                    # Plain text version (important for spam filters!)
                    mail_message.add_content(f'''
New Contact Form Submission

From: {name}
Email: {email}

Message:
{message}

---
Reply to this email to respond directly to {name}.
                    '''.strip(), 'text/plain')
                    
                    # HTML version
                    mail_message.add_content(f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #f8f9fa; border-radius: 8px; padding: 30px; margin: 20px 0;">
        <h2 style="color: #2563eb; margin-top: 0; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">
            New Portfolio Contact
        </h2>
        
        <div style="background-color: white; border-radius: 6px; padding: 20px; margin: 20px 0; border-left: 4px solid #2563eb;">
            <p style="margin: 10px 0;"><strong style="color: #555;">From:</strong> {name}</p>
            <p style="margin: 10px 0;"><strong style="color: #555;">Email:</strong> <a href="mailto:{email}" style="color: #2563eb; text-decoration: none;">{email}</a></p>
        </div>
        
        <div style="background-color: white; border-radius: 6px; padding: 20px; margin: 20px 0;">
            <p style="margin: 0 0 10px 0;"><strong style="color: #555;">Message:</strong></p>
            <p style="margin: 0; white-space: pre-wrap; color: #333;">{message}</p>
        </div>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; font-size: 14px;">
            <p style="margin: 5px 0;">💡 Click reply to respond directly to {name}</p>
            <p style="margin: 5px 0;">📧 Sent from your portfolio contact form</p>
        </div>
    </div>
</body>
</html>
                    '''.strip(), 'text/html')
                    
                    # Disable click tracking and open tracking to reduce spam score
                    from sendgrid.helpers.mail import TrackingSettings, ClickTracking, OpenTracking
                    mail_message.tracking_settings = TrackingSettings()
                    mail_message.tracking_settings.click_tracking = ClickTracking(False, False)
                    mail_message.tracking_settings.open_tracking = OpenTracking(False)
                    
                    sg = SendGridAPIClient(sendgrid_api_key)
                    response = sg.send(mail_message)
                    print(f"✅ SendGrid email sent! Status: {response.status_code}")
                    print(f"📧 Response body: {response.body}")
                    print(f"📋 Response headers: {response.headers}")
                    print(f"✅ Email sent to: sushilchavan2468@gmail.com from: {name} ({email})")
                else:
                    # Fallback to Gmail SMTP (ONLY works locally, NOT on Render)
                    print("⚠️ No SendGrid key found, trying Gmail SMTP (won't work on Render)")
                    subject = f"New Contact Message from {name}"
                    body = f"""You received a new message from your website contact form.

Name: {name}
Email: {email}
Message:
{message}"""
                    
                    email_msg = EmailMessage(
                        subject=subject,
                        body=body,
                        from_email=settings.EMAIL_HOST_USER,
                        to=['sushilchavan2468@gmail.com'],
                        headers={'Reply-To': email}
                    )
                    email_msg.send(fail_silently=True)
                    print("✅ Gmail SMTP attempted (only works locally)")
                    
            except Exception as e:
                print(f"❌ Email error: {e}")
                print(f"❌ Error type: {type(e).__name__}")
                import traceback
                print(f"❌ Full traceback: {traceback.format_exc()}")
                pass  # Email failed, but that's okay - message is in database
            
            return render(request, 'contact.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def projects_view(request):
    """View to display all projects page"""
    return render(request, 'projects.html')

# .\env\Scripts\Activate.ps1
# env\Scripts\activate 
# python manage.py runserver          