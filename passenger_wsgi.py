import os
import sys

# Add project directory to sys.path
sys.path.insert(0, "/home/hightech/azamericanestatebuyer.com/printing")

# Add virtualenv site-packages
sys.path.insert(0, "/home/hightech/virtualenv/azamericanestatebuyer.com/printing/3.10/lib/python3.10/site-packages")

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "printing.settings")

# Activate virtualenv (optional but recommended)
activate_this = "/home/hightech/virtualenv/azamericanestatebuyer.com/printing/3.10/bin/activate_this.py"
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
