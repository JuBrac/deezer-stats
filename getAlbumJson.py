import json
import pandas as pd
import time
import requests

dataframes = pd.read_excel("full_history.xlsx",sheet_name=None,engine='openpyxl')
full_history = dataframes['10_listeningHistory']

output_history = full_history.groupby(['Song Title','Artist','ISRC']).size().reset_index(name="Nombre d'écoutes").sort_values(by="Nombre d'écoutes",ascending=False)

album_history = full_history.groupby(["Album Title"]).size().reset_index(name = "Nombre d'écoutes")

'''Creation de album.json'''
album_json = {}
for indexAlbum,rowAlbum in album_history.iterrows():
    album = full_history[full_history["Album Title"]==rowAlbum["Album Title"]].iloc[0]
    info_track = requests.get('https://api.deezer.com/2.0/track/isrc:'+album["ISRC"])
    while(info_track.status_code != 200):
        time.sleep(1)
        info_track = requests.get('https://api.deezer.com/2.0/track/isrc:'+album["ISRC"])

    json_track = json.loads(info_track.text)
    album_json[album["Album Title"]] = json_track["album"]["id"]
    compteur = compteur+1

with open("album.json","w") as album_id:
    album_id.write(json.dumps(album_json,indent=1))

'''Requêtes sur chaque album'''
with open("album.json","r") as album_id:
    album_json = album_id.read()
    album_json =json.loads(album_json)

for album,id in album_json.items():
    info_album = requests.get('https://api.deezer.com/2.0/album/'+str(id))
    json_album = json.loads(info_album.text)
    try:
        new_album = {album:[id,json_album["nb_tracks"],json_album["cover_medium"]]}
        album_json.update(new_album)
    except:
        print("L'album n'existe plus.")

with open("album_full.json","w") as album_id:
    album_id.write(json.dumps(album_json,indent=1))