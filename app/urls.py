from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.WatchListView.as_view(), name='watchlist'),
    path('oi/<str:symbol>/', views.OIView.as_view(), name='oi'),
    path('historical/', views.HistoricalView.as_view(), name='historical'),
]
