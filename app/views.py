from django.shortcuts import render
from django.views import View
from django.views.generic.list import MultipleObjectTemplateResponseMixin

from app.utils import get_watchlist

class WatchListView(MultipleObjectTemplateResponseMixin, View):

    template_name = 'main_page.html'

    def get(self, request):
        search = request.GET.get('search', False)
        vol_change_min = request.GET.get('vol_change_min', default=None)
        dom_min = request.GET.get('dom_min', default=None)
        vol_per_mcap_min = request.GET.get('vol_per_mcap_min', default=None)
        watchlist = get_watchlist(search, vol_change_min, dom_min, vol_per_mcap_min)
        ctx = { 
            'watchlist': watchlist, 
            'search': search,
            'vol_change_min': vol_change_min,
            'dom_min': dom_min,
            'vol_per_mcap_min': vol_per_mcap_min
            }
        return render(request, self.template_name, ctx)
