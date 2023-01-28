from django.shortcuts import render
from django.views import View
from django.views.generic.list import MultipleObjectTemplateResponseMixin

from app.utils import get_watchlist

class WatchListView(MultipleObjectTemplateResponseMixin, View):

    template_name = 'main_page.html'

    def get(self, request):
        watchlist = get_watchlist()
        ctx = { 'watchlist': watchlist }
        return render(request, self.template_name, ctx)
