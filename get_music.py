import argparse
import requests
import json
import sys
import os

# Parsing input arguments
parser = argparse.ArgumentParser()
parser.add_argument('song_json_file', type=argparse.FileType('r'))
args = parser.parse_args()
song_list = json.load(args.song_json_file)

# Get the html response from the songurl
qury = requests.get(str(song_list["songurl"]))
assert qury.status_code == 200
quryhtml_str = str(qury.content)

# Dirty parsing the mp3url out from the html
starter = 0
mp3dest = 0
padding = 8
while quryhtml_str.find("mp3url=\"",starter) is not -1:
	mp3dest = quryhtml_str.find("mp3url=\"", starter)
	if quryhtml_str[mp3dest+padding] == "\"":
		starter = mp3dest + padding
	else:
		break

url_head = mp3dest + padding
url_tail = quryhtml_str.find("\"",url_head)
mp3url = quryhtml_str[url_head:url_tail]

# Fetch the mp3 file from the mp3url
resp = requests.get(mp3url)
assert resp.status_code == 200
with open(str(song_list["savename"]), 'wb') as f:
	f.write(resp.content)
