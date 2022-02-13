import re
import time
import typer
import requests
import json

app = typer.Typer()
# artist_app = typer.Typer()
# app.add_typer(artist_app, name="artist")

def api_call(url):
    http = requests.Session()
    assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
    http.hooks['response'] = [assert_status_hook]

    try:
        response = http.get(url, timeout=30)
        # response = requests.get(url, timeout=30)
    except requests.exceptions.Timeout as errt:
        typer.echo(f"Connection timeout")
        raise SystemExit(errt)
    except requests.exceptions.TooManyRedirects as errr:
        typer.echo(f"Too many redirects")
        raise SystemExit(errr)
    except requests.exceptions.HTTPError as errh:
        # typer.echo(errh)
        pass
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    else:
        json_data = json.loads(response.content)
        return json_data


@app.command()
def main(artist: str, limit: int = 25):
    # Musicbrainz API query limit is 100
    if limit <= 100 or limit >= 1:
        """
        search artist name
        """
        typer.echo(f"Searching artist(s)...")
        typer.echo(f"")
        url = 'https://musicbrainz.org/ws/2/artist/?query="' + artist + '"&fmt=json'
        json_data = api_call(url)

        if json_data and 'error' not in json_data and 'count' in json_data and json_data['count'] > 0:
            
            """
            match query string with first record
            """
            artist_id = json_data['artists'][0]['id']
            artist = json_data['artists'][0]['name']

            typer.echo(f"{len(json_data['artists'])} record(s) found.")
            typer.echo(f"First record chosen by default: ")
            typer.echo(f"Artist name: {artist}")
            typer.echo(f"Artist MBID: {artist_id}")
            typer.echo(f"")

            """
            get releases
            """
            typer.echo(f"Searching for album(s)...")
            url = 'https://musicbrainz.org/ws/2/release?artist=' + artist_id + '&limit=' + str(limit) + '&fmt=json'
            # url = 'https://musicbrainz.org/ws/2/artist/' + artist_id + '?inc=releases&fmt=json'
            json_data = api_call(url)
            json.dumps(json_data, indent=4)
            number_of_record = len(json_data['releases'])
            typer.echo(f"{number_of_record} record(s) found.")
            typer.echo(f"")


            """
            get songs
            """
            typer.echo(f"Searching for song(s)...")
            with typer.progressbar(json_data['releases']) as progress:
                songs = set()
                for release in progress:
                    url = 'https://musicbrainz.org/ws/2/release/' + release['id'] + '?inc=recordings&fmt=json'
                    json_data = api_call(url)
                    if json_data and 'media' in json_data:
                        if 'tracks' in json_data['media'][0]:
                            for track in json_data['media'][0]['tracks']:
                                if 'title' in track:
                                    songs.add(track['title'])
                    # musicbrainz api call time limit 1 call/sec
                    time.sleep(1)
            typer.echo(f"")
            

            """
            get lyrics
            """
            typer.echo(f"Processing lyrics length...")
            songs_length = []
            song_list = list(songs)
            with typer.progressbar(song_list) as progress:
                for song in progress:
                    url = 'https://api.lyrics.ovh/v1/' + artist + '/' + song
                    json_data = api_call(url)
                    if json_data and 'lyrics' in json_data:
                        lyrics = json_data['lyrics']
                        lyrics = re.sub(r"[,@!?\.$%_]", "", lyrics, flags=re.I)
                        lyrics = re.sub(r"\s+"," ", lyrics, flags=re.I)
                        result = lyrics.split()
                        songs_length.append(len(result))
            typer.echo(f"")

            """
            get average lyrics length
            """
            if songs_length:
                list_length = len(songs_length)
                list_sum = sum(songs_length)
                average_length = list_sum/list_length
                typer.echo(f"Out of {list_length} successful lyrics search, average number of words in songs by {artist} is {round(average_length)} words.")
            else:
                typer.echo(f"Failed to retrieve any lyrics")
        else:
            typer.echo(f"No matching artist found")
    else:
        typer.echo(f"Limit has to be 1 <= limit <= 100")

if __name__ == "__main__":
    app()