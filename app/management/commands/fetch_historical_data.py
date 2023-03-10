from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from app.models import Historical
from app.utils.cmc import get_watchlist

class Command(BaseCommand):
    help = "Fetch historical data from the CMC API to the database"
    def fetch(self):
        page_size = 5000
        page = 1
        count, data = get_watchlist(None, None, None, None, page, page_size)
        total_data: list = data
        while len(data) != 0:
          page += 1
          count, data = get_watchlist(None, None, None, None, page, page_size)
          total_data.extend(data)
        for e in total_data:
          Historical.objects.create(name=e["Name"], symbol=e["Symbol"], 
                              price=e["Price"], volume=e["Volume 24h"], dominance=e["Market cap dominance"], volume_divided_market=(e["Volume 24h / market cap"]))
    
    def delete_old_records(self):
        thirty_days_ago = datetime.now() - timedelta(days=30)
        old_records = Historical.objects.filter(created_at__date__lte=thirty_days_ago)
        old_records.delete()
    
    def handle(self, *args, **options):
        self.fetch()
        self.delete_old_records()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved historical data'))