from datetime import datetime, date, timedelta
import pytz
from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.views.generic.list import MultipleObjectTemplateResponseMixin
from app.models import Historical
from app.utils.cg import get_oi
from app.utils.cmc import CMC_CURRENCY_URL, get_watchlist
from app.utils.historical import convert_historical_query

class WatchListView(MultipleObjectTemplateResponseMixin, View):
    template_name = 'main_page.html'

    def get(self, request):
        search = request.GET.get('search', False)
        vol_change_min = request.GET.get('vol_change_min', default=None)
        dom_min = request.GET.get('dom_min', default=None)
        vol_per_mcap_min = request.GET.get('vol_per_mcap_min', default=None)
        market_cap_min = request.GET.get('market_cap_min', default=None)
        page = request.GET.get('page', default=1)
        page_size = int(request.GET.get('page_size', default=100))
        count, watchlist = get_watchlist(search, vol_change_min, dom_min, vol_per_mcap_min, page, page_size, market_cap_min)
        ctx = { 
            'watchlist': watchlist, 
            'search': search,
            'vol_change_min': vol_change_min,
            'dom_min': dom_min,
            'vol_per_mcap_min': vol_per_mcap_min,
            'page': page,
            'page_size': page_size,
            'num_of_pages': int(count / page_size) + 1,
            'cmc_url': CMC_CURRENCY_URL,
            "market_cap_min": market_cap_min
            }
        return render(request, self.template_name, ctx)

class OIView(MultipleObjectTemplateResponseMixin, View):
    template_name = 'oi_page.html'

    def get(self, request, symbol):
        oi_data = get_oi(symbol)
        ctx = {
            'oi_data': oi_data,
            'symbol': symbol,
        }
        return render(request, self.template_name, ctx)

class HistoricalView(MultipleObjectTemplateResponseMixin, View):
    template_name = 'historical_page.html'

    def get(self, request):
        search = request.GET.get('search')
        start_date_str = request.GET.get('start_date') 
        end_date_str = request.GET.get('end_date')
        price = request.GET.get('price', default=None)
        volume = request.GET.get('volume', default=None)
        dominance = request.GET.get('dominance', default=None)
        volume_divided_market = request.GET.get('volume_divided_market', default=None)

        tz = pytz.timezone('UTC')
        yesterday = datetime.combine(date.today() - timedelta(days=1), datetime.min.time())
        today = datetime.combine(date.today(), datetime.min.time())

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else yesterday
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else today

        start_date = tz.localize(start_date)
        end_date = tz.localize(end_date)
        if start_date and end_date and search:
            query = Historical.objects.filter(Q(created_at__date=start_date) | Q(created_at__date=end_date), name__icontains=search)
        elif start_date and end_date and not search:
            query = Historical.objects.filter(Q(created_at__date=start_date) | Q(created_at__date=end_date))

        historical_list = convert_historical_query(list(query), price, volume, dominance, volume_divided_market)
        ctx = {
            'search': search,
            'start_date': start_date,
            'end_date': end_date,
            'historical_list': historical_list,
            'price': price,
            'volume': volume,
            'dominance': dominance,
            "volume_divided_market": volume_divided_market,
            'cmc_url': CMC_CURRENCY_URL
        }
        return render(request, self.template_name, ctx)