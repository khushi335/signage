import os
import sys

# Add your project directory to the sys.path
project_home = "/home/hightech/project.azamericanestatebuyer.com/printing"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = "/home/hightech/virtualenv/project.azamericanestatebuyer.com/printing/3.10/bin/activate_this.py"
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "printing.settings")

# Import WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()