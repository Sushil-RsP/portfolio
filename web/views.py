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
                    from sendgrid.helpers.mail import Mail
                    
                    # Simple, clean format that works reliably
                    plain_text = f'''New Contact Form Submission

From: {name}
Email: {email}

Message:
{message}

---
Reply to this email to respond directly to {name}.'''

                    html_content = f'''<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto; padding: 20px;">
    <h2 style="color: #333;">New Contact Form Submission</h2>
    <div style="background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0;">
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Message:</strong></p>
        <p style="white-space: pre-wrap; background: white; padding: 15px; border-left: 4px solid #007bff;">{message}</p>
    </div>
</div>'''

                    mail_message = Mail(
                        from_email='sushilchavan2468@gmail.com',
                        to_emails='sushilchavan2468@gmail.com',
                        subject=f'Portfolio Contact from {name}',
                        plain_text_content=plain_text,
                        html_content=html_content
                    )
                    
                    # Set reply-to
                    mail_message.reply_to = email
                    
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