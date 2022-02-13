# average_length_lyrics

average_lyrics_length is a CLI application that, through interaction with Musicbrainz and lyrics.ovh API, produces the average
(mean) number of words in an artist's songs.

## Installation

Please install the required libraries if necessary

```bash
pip install requests
pip install typer
```

## Usage

In the app folder 

```bash
# run the app
# artist: artist name (for names with space, use quote e.g. "artist name")
python main.py artist

# self define maximum number of records to return (1 <= limit <= 100)
python main.py artist --limit 100

# help page
python main.py artist --help

```