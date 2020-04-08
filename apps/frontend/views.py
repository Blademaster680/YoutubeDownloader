import pafy
from django.shortcuts import render
from django.template.defaultfilters import filesizeformat


def index(request):

    return render(request, 'frontend/index.html')

def video_detail(request):
    """
    Gets the URL that was pasted in from the home page and pulls
    it through pafy to process the URL as a youtube video.
    """
    url = request.POST.get('video')
    video = pafy.new(url)

    stream = video.streams
    video_audio_streams = []
    for s in stream:
        video_audio_streams.append({
            'resolution': s.resolution,
            'extension': s.extension,
            'file_size': filesizeformat(s.get_filesize()),
            'video_url': s.url + "&title" + video.title
        })

    stream_audio = video.audiostreams
    audio_streams = []
    for s in stream_audio:
        audio_streams.append({
            'resolution': s.resolution,
            'extension': s.extension,
            'file_size': filesizeformat(s.get_filesize()),
            'video_url': s.url + "&title" + video.title
        })

    context = {
        'title': video.title,
        'thumbnail': video.bigthumbhd,
        'description': video.description,
        'stream_audio': video.getbestaudio(), 'streams': video_audio_streams,
        'hd_stream': video.getbestvideo(),
        'hd_url': video.getbestvideo().url + "&title" + video.getbestvideo().title
    }
    return render(request, 'frontend/video-detail.html', context)
