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

            # Try to send email using SendGrid
            try:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']

                # Check if SendGrid API key is configured
                sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
                
                if sendgrid_api_key:
                    # Use SendGrid API (works on Render free tier)
                    from sendgrid import SendGridAPIClient
                    from sendgrid.helpers.mail import Mail
                    
                    mail_message = Mail(
                        from_email='sushilchavan2468@gmail.com',
                        to_emails='sushilchavan2468@gmail.com',
                        subject=f'New Contact Message from {name}',
                        html_content=f'''
                        <h3>New Contact Form Submission</h3>
                        <p><strong>Name:</strong> {name}</p>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Message:</strong></p>
                        <p>{message}</p>
                        '''
                    )
                    
                    sg = SendGridAPIClient(sendgrid_api_key)
                    sg.send(mail_message)
                else:
                    # Fallback to SMTP (only works locally, not on Render)
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
            except:
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