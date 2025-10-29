import os
import django
import sys

# Add the project directory to the path
sys.path.insert(0, r'D:\Pictures\portfolio')

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
os.environ['DEBUG'] = 'True'
os.environ['SECRET_KEY'] = 'test-secret-key-for-debugging'

django.setup()

# Now test the view
from django.test import RequestFactory
from web.views import contact_view

factory = RequestFactory()
request = factory.get('/')

try:
    response = contact_view(request)
    print(f"Response status: {response.status_code}")
    if response.status_code == 200:
        print("✓ View works correctly!")
    else:
        print(f"✗ Got status {response.status_code}")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
