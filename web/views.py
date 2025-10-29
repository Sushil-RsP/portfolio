# Create your views here.

# contact/views.py

from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from .forms import ContactForm
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def contact_view(request):
    logger.info(f"Contact view called with method: {request.method}")
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                # Save the form data to database first
                form.save()

                # Send Email
                # Get the cleaned data
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']

                # Compose email
                subject = f"New Contact Message from {name}"
                body = f"""You received a new message from your website contact form.

Name: {name}
Email: {email}
Message:
{message}"""
                recipient_list = ['sushilchavan2468@gmail.com']

                # Use EmailMessage to set reply-to
                email_msg = EmailMessage(
                    subject=subject,
                    body=body,
                    to=recipient_list,
                    headers={'Reply-To': email}  # So you can reply directly to sender
                )
                email_msg.send(fail_silently=False)
                
                logger.info(f"Email sent successfully from {name} ({email})")
                return render(request, 'contact.html', {'form': ContactForm(), 'success': True})
            
            except Exception as email_error:
                # Log the email error but don't crash - form is already saved
                logger.error(f"Failed to send email: {email_error}", exc_info=True)
                # Still show success to user since their message was saved
                return render(request, 'contact.html', {'form': ContactForm(), 'success': True, 'email_failed': True})
        else:
            logger.warning(f"Form validation failed: {form.errors}")
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def projects_view(request):
    """View to display all projects page"""
    return render(request, 'projects.html')

# .\env\Scripts\Activate.ps1
# env\Scripts\activate 
# python manage.py runserver          