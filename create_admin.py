import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AI_Customer_Support_Ticket_System.settings')
django.setup()

from django.contrib.auth.models import User

username = "admin"
email = "rajeevannandana7@gmail.com"
password = "webverse@4"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("Superuser created!")
else:
    print("Superuser already exists.")