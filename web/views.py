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
            # Save the form data to database first
            form.save()
            
            print("=== STARTING EMAIL SEND ===")
            print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
            print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
            print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")

            try:
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

                print(f"Attempting to send email to: {recipient_list}")
                
                # Use EmailMessage to set reply-to
                email_msg = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=settings.EMAIL_HOST_USER,  # Add from_email
                    to=recipient_list,
                    headers={'Reply-To': email}  # So you can reply directly to sender
                )
                
                result = email_msg.send(fail_silently=False)  # Show errors if email fails
                print(f"✅ Email send result: {result}")
                print(f"✅ Email sent successfully to: {recipient_list}")
                
            except Exception as e:
                # Email failed, but form is saved - that's okay
                print(f"❌ EMAIL ERROR: {str(e)}")
                print(f"❌ Error type: {type(e).__name__}")
                import traceback
                print(f"❌ Full traceback:\n{traceback.format_exc()}")
                pass
            
            print("=== EMAIL SEND COMPLETE ===")
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