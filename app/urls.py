from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.WatchListView.as_view(), name='watchlist'),
]