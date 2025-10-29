# Create your views here.

# contact/views.py

from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from .forms import ContactForm
from django.conf import settings

def contact_view(request):
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
                email_msg.send(fail_silently=True)  # Don't crash if email fails
                
                return render(request, 'contact.html', {'form': ContactForm(), 'success': True})
            
            except Exception as e:
                # If anything fails, still save the form and show success
                # Message is saved to database, that's what matters
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