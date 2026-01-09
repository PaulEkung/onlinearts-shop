from django.db import connection
import os
import sys
import django

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artisan.settings')
try:
    django.setup()
except ImportError:
    print("Django is not set up correctly")
    

with connection.cursor() as cursor:
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS `artisan`"
    )
    if cursor:
        print("Database created successfully")
    else:
        print("Failed to create database")


