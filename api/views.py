# api/views.py

from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views import View
from yt_dlp import YoutubeDL
import ffmpeg
import os

class DownloadVideoView(APIView):
    def post(self, request):
        url = request.data.get('url')
        if not url:
            return JsonResponse({'error': 'URL is required'}, status=400)

        try:
            ydl_opts = {
                'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(title)s.%(ext)s'),
                'format': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
            }
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                title = info_dict.get('title', None)
                thumb_video = info_dict.get('thumbnail', None)
                video_title = title.replace(' ', '_')
                video_title = video_title.replace('#', '_')
                video_title = video_title.replace('?', '_')
                video_filename = ydl.prepare_filename(info_dict)

            mp4_path = os.path.join(settings.MEDIA_ROOT, f"{video_title}.mp4")
            if os.path.exists(mp4_path):
                converter = False
            else:
                converter = True

            if converter:
                ffmpeg.input(video_filename).output(mp4_path).overwrite_output().run()

            download_url = request.build_absolute_uri(settings.MEDIA_URL + f"{video_title}.mp4")
            return JsonResponse({"download_url": download_url, "title": title, "thumb_video": thumb_video})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')
