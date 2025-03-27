from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = settings.CONFIG["DB_USER"]
        password = settings.CONFIG["DB_PASSWORD"]

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password)