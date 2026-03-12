import os
import sys

# Add project directory to Python path
sys.path.insert(0, '/home/hightech/azamericanestatebuyer.com/printing')

# Activate virtual environment
activate_this = '/home/hightech/virtualenv/azamericanestatebuyer.com/printing/3.10/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Set Django settings module (change if your project name is different)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printing.settings')

# Load Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()