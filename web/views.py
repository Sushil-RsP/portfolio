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
    try:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()

                # Send Email
                # Get the cleaned data
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']

                # Compose email
                subject = f"New Contact Message from {name}"
                body = f"""
            You received a new message from your website contact form.
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

                return render(request, 'contact.html', {'form': form, 'success': True})
        else:
            form = ContactForm()
        return render(request, 'contact.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in contact_view: {e}", exc_info=True)
        raise

def projects_view(request):
    """View to display all projects page"""
    return render(request, 'projects.html')

# .\env\Scripts\Activate.ps1
# env\Scripts\activate 
# python manage.py runserver          