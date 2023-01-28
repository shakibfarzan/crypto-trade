from django.shortcuts import render
from django.views import View
from django.views.generic.list import MultipleObjectTemplateResponseMixin

from app.utils import get_watchlist

class WatchListView(MultipleObjectTemplateResponseMixin, View):

    template_name = 'main_page.html'

    def get(self, request):
        search = request.GET.get('search', False)
        watchlist = get_watchlist(search)
        ctx = { 'watchlist': watchlist, 'search': search }
        return render(request, self.template_name, ctx)
