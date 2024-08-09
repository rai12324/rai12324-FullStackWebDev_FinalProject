# Replace 'your_username' with your actual PythonAnywhere username
import sys
import os

# Add the directory containing your Flask application to the Python path
project_home = '/home/Cabibi12324/mysite'  # Change this to your actual project directory
if project_home not in sys.path:
    sys.path.append(project_home)

# Import your Flask application instance
from app import app as application
