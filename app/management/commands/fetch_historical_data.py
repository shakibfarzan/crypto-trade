from django.core.management.base import BaseCommand
from app.utils import handle_fetch_command

class Command(BaseCommand):
    help = "Fetch historical data from the CMC API to the database"
    def handle(self, *args, **options):
        handle_fetch_command()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved historical data'))