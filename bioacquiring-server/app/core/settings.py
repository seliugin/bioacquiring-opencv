import os

# Database configuration
DATABASE = {
    'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
    'PORT': os.environ.get('DATABASE_PORT', 5432),
    'NAME': os.environ.get('DATABASE_NAME', 'badb'),
    'USER': os.environ.get('DATABASE_USER', 'bauser'),
    'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'unsafe-password123')
}