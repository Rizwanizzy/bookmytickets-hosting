import os
import sys

from django.core.asgi import get_asgi_application
from daphne.server import Server

# Load the Django ASGI application
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Book_my_show.settings')
django_application = get_asgi_application()

# Start the Daphne server
server = Server(django_application)
server.run(port='8000')  # Set the desired port number

