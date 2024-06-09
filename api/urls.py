# api/urls.py

from django.urls import path
from .views import DownloadVideoView, HomeView

urlpatterns = [
    path('api/download/', DownloadVideoView.as_view(), name='download-video'),
    path('', HomeView.as_view(), name='home'),
]
