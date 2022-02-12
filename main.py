import time
import requests
import json
import re

class Lyrics:
    def __init__(self):
        self.artist = None

    def get_artist(self):
        self.artist = 'Coldplay'
        


        url = 'https://musicbrainz.org/ws/2/artist/?query="' + artist + '"&fmt=json'
        response = requests.get(url)
        json_data = json.loads(response.content)
        # print(json.dumps(json_data['artists'][0]['id'], indent=4, sort_keys=True))

    def get_releases(self):


        url = 'https://musicbrainz.org/ws/2/artist/' + json_data['artists'][0]['id'] + '?inc=releases&fmt=json'
        response = requests.get(url)
        json_data = json.loads(response.content)
        # print(json.dumps(json_data, indent=4, sort_keys=True))

songs = set()
for release in json_data['releases']:
    url = 'https://musicbrainz.org/ws/2/release/' + release['id'] + '?inc=recordings&fmt=json'
    response = requests.get(url)
    json_data = json.loads(response.content)
    # print(json_data['media'][0])
    try:
        # print(json.dumps(json_data['media'][0]['tracks'], indent=4, sort_keys=True))
        for track in json_data['media'][0]['tracks']:
            songs.add(track['title'])
    except:
        print(json.dumps(json_data, indent=4, sort_keys=True))
    time.sleep(1)
    

results = []
songs_list = list(songs)
for i in range(len(songs_list)):
    url = 'https://api.lyrics.ovh/v1/' + artist + '/' + songs_list[i]
    try:
        response = requests.get(url)
        json_data = json.loads(response.content)
        lyrics = json_data['lyrics']
        lyrics = re.sub(r"[,@!?\.$%_]", "", lyrics, flags=re.I)
        lyrics = re.sub(r"\s+"," ", lyrics, flags = re.I)
        result = lyrics.split()
        results.append(len(result))
    except:
        continue

print(sum(results)/len(results))    
    def get_songs(self):
        pass
    def get_average(self):
        pass