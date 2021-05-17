# Description
Sometimes websites embed hidden/private videos from Vimeo in order to prevent the download of these videos. This technique is often used behind paywall or similar access restriction. You can recognize such a video by the missing Share button within the vimeo video player. This Python 3 script enables you to download such videos in full quality.

First you need to identify the URL, which the video player uses to get the video data. You can accomplish this by opening your Browser's developer tools (F12) and going to the network tab. Next you need to search for a URL request to an URL, which should look similar (sometimes a base64 string is appended to the master.json, just remove it) to the following:

```
https://<something>.akamaized.net/exp=<numbers>~acl=%<guid>%2F%2A~hmac=<hmac>/<guid>/sep/video/<id>,<id>,<id>,<id>/master.json
```

The first request to the master.json file is usually performed when hovering over the video player. The master.json file specifies the number and lengths of the segments of the video. This script downloads all segments and concatenates them to construct the full mp4 video file. Use the following command to download the video:

```
python3 vimeo-downloader.py https://<something>.akamaized.net/exp=<numbers>~acl=%<guid>%2F%2A~hmac=<hmac>/<guid>/sep/video/<id>,<id>,<id>,<id>/master.json
```

Last, the audio and the video file need to be merged with ffmpeg. The script prints the correct command for this operation. Just execute it and you are done.


# References
* https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP
* https://gist.github.com/mistic100/895f6d17b1e193334882a4c37d0d7748
* https://www.ffmpeg.org/
* https://superuser.com/questions/1349502/what-is-the-format-of-the-mpeg-dash-m4s-generally-segment