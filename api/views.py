# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pytube import YouTube
import os
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

class DownloadVideoView(APIView):
    def post(self, request, *args, **kwargs):
        video_url = request.data.get("url")
        if not video_url:
            return Response({"error": "URL do vídeo é necessária"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            yt = YouTube(video_url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            file_path = stream.download(output_path=settings.MEDIA_ROOT)
            file_name = os.path.basename(file_path)
            download_url = request.build_absolute_uri(settings.MEDIA_URL + file_name)
            title = yt.title
            thumb_video = yt.thumbnail_url
            
            return JsonResponse({"download_url": download_url, "title": title, "thumb_video": thumb_video}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')
