from django.shortcuts import render
from django.views import View
from django.views.generic.list import MultipleObjectTemplateResponseMixin

from app.utils import get_oi, get_watchlist

class WatchListView(MultipleObjectTemplateResponseMixin, View):
    template_name = 'main_page.html'

    def get(self, request):
        search = request.GET.get('search', False)
        vol_change_min = request.GET.get('vol_change_min', default=None)
        dom_min = request.GET.get('dom_min', default=None)
        vol_per_mcap_min = request.GET.get('vol_per_mcap_min', default=None)
        page = request.GET.get('page', default=1)
        page_size = int(request.GET.get('page_size', default=100))
        count, watchlist = get_watchlist(search, vol_change_min, dom_min, vol_per_mcap_min, page, page_size)
        ctx = { 
            'watchlist': watchlist, 
            'search': search,
            'vol_change_min': vol_change_min,
            'dom_min': dom_min,
            'vol_per_mcap_min': vol_per_mcap_min,
            'page': page,
            'page_size': page_size,
            'num_of_pages': int(count / page_size) + 1,
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