#!/usr/bin/python3
import requests
import json
import os
import shutil
import sys

if len(sys.argv) != 2:
    print("Wrong number of arguments")
    print("python3 vimeo-downloader.py <url of master.json>")
    exit()

master_json_url = sys.argv[1]
print(master_json_url)


def parse_json(json_text):
    global clip_id, audio_id, video_id, number_of_segments, segment_base_name, segment_base_ext
    json_data = json.loads(json_text)
    clip_id = json_data["clip_id"]
    video_id = json_data["video"][0]["id"]
    audio_id = json_data["video"][0]["id"]
    number_of_segments = len(json_data["video"][0]["segments"])
    segment_base_name, segment_base_ext = json_data["video"][0]["segments"][0]["url"].split("1")


base_url = master_json_url.split("video/")[0]
print(base_url)
clip_id = ""
audio_id = ""
video_id = ""
number_of_segments = ""
segment_base_name = ""
segment_base_ext = ""


r = requests.get(master_json_url)

parse_json(r.text)

out_video = "segments_video_" + clip_id
out_audio = "segments_audio_" + clip_id
try:
    shutil.rmtree(out_video)
    shutil.rmtree(out_audio)
except:
    pass

if not os.path.exists(out_video):
    os.mkdir(out_video)
if not os.path.exists(out_audio):
    os.mkdir(out_audio)

print("Clip_ID: " + str(clip_id))
print("Video_ID: " + str(video_id))
print("Audio_ID: " + str(audio_id))
print("Number of Segments: " + str(number_of_segments) )
print()
print("Start Download")
full_video = b""
full_audio = b""
for i in range(0, number_of_segments+1):
    # video
    current_segement_url = base_url + "video/" + str(video_id) + "/chop/" + segment_base_name + str(i) + segment_base_ext
    r = requests.get(current_segement_url)
    with open(os.path.join(out_video ,"video-" + segment_base_name + str(i) + segment_base_ext), "wb") as f:
        f.write(r.content)
    full_video += r.content

    # audio
    current_segement_url = base_url + "audio/" + str(video_id) + "/chop/" + segment_base_name + str(i) + segment_base_ext
    r = requests.get(current_segement_url)
    with open(os.path.join(out_audio ,"audio-" + segment_base_name + str(i) + segment_base_ext), "wb") as f:
        f.write(r.content)
    full_audio += r.content

    if i % 10 == 0:
        print(str(i) + "/" + str(number_of_segments) + " downloaded")

with open(video_id + "_final_video.mp4", "wb") as f:
    f.write(full_video)

with open(video_id + "_final_audio.mp4", "wb") as f:
    f.write(full_audio)

print("Merge the output files with the following command:")
print("$ ffmpeg -i " + video_id + "_final_video.mp4" + " -i " + video_id + "_final_audio.mp4" + " -c copy " + clip_id + "final_video.mp4")