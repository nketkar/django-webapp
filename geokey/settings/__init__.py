import os

# Import the defaults and common settings
from .base import *

# Load development settings based on DJANGO_MODE environment variable
if os.environ.get('DJANGO_MODE', 'PRODUCTION') == 'DEVELOPMENT':
    from .development import *
else:
    from .production import *

# Try and import local settings which can be used to override any of the above.
try:
    from .local import *
except ImportError:
    pass
