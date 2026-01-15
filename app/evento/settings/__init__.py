import os

# Determine which settings to use based on environment variable
# Default to development if not specified
environment = os.getenv('ENVIRONMENT', 'development')

if environment == 'development':
    from .development import *
else:
    from .base import *
