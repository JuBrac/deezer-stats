from os import write
import os
from datetime import date,datetime
from matplotlib import pyplot as plt
import pandas as pd
import json
import july
from july.utils import date_range

TOP_NUMBER = 100 #taille des listes à sauvegarder

'''Ouverture de l'historique'''
dataframes = pd.read_excel("full_history.xlsx",sheet_name=None,engine='openpyxl')
full_history = dataframes['10_listeningHistory']

output_history = full_history.groupby(['Song Title','Artist','ISRC']).size().reset_index(name="Nombre d'écoutes").sort_values(by="Nombre d'écoutes",ascending=False)
album_history = full_history.groupby(["Album Title"]).size().reset_index(name = "Nombre d'écoutes")


'''Calcul du ratio d'écoutes'''
with open("album_full.json","r") as album_info:
    full_album_json = album_info.read()
    full_album_json = json.loads(full_album_json)

tracks = []
for album,id in full_album_json.items():
    try:
        tracks.append(id[1])
    except:
        tracks.append(-1)

album_history["Nombre tracks"] = tracks
album_history["Ratio d'écoutes"] = album_history.apply(lambda x:int(x[1])/int(x[2]),axis=1)

album_history = album_history.sort_values(by="Ratio d'écoutes",ascending=False)
# print(album_history[album_history["Nombre tracks"]>5].iloc[:TOP_NUMBER]) #>5 pour éviter les EPs trop court et aussi quelques bugs (ex : Horizon Vertical)
album_ratio = album_history[album_history["Nombre tracks"]>5].iloc[:TOP_NUMBER]

output_history = full_history.groupby(['Song Title','Artist','ISRC']).size().reset_index(name="Nombre d'écoutes").sort_values(by="Nombre d'écoutes",ascending=False)
# print(output_history.iloc[:TOP_NUMBER])
title_top = output_history.iloc[:TOP_NUMBER]

album_history = full_history.groupby(["Album Title"]).size().reset_index(name = "Nombre d'écoutes").sort_values(by="Nombre d'écoutes",ascending=False)
# print(album_history.iloc[:TOP_NUMBER])
album_top = album_history.iloc[:TOP_NUMBER]

'''Création d'un calendrier d'écoutes'''
listeningYear = "2021"

date_history = full_history
date_history["Date"] = date_history["Date"].apply(lambda x: pd.Timestamp(year = x.year,month = x.month, day= x.day))
date_history = full_history.groupby(["Date"]).size().reset_index(name="Nombre d'écoutes").sort_values(by="Date",ascending=True)

listening_calendar = pd.Series(date_history["Nombre d'écoutes"],index = date_history["Date"])

date_history = date_history.loc[date_history["Date"].astype(str).str.find(listeningYear)!=-1]

'''Utilisation de july pour générer la calendar map'''
dates = date_range("2021-01-01", "2021-07-14")
july.heatmap(date_history["Date"], date_history["Nombre d'écoutes"], title='Ecoute Deezer', cmap="github")
# plt.show()

'''Calcul du nombre de minutes écoutés par jour sur une année précise.'''
date_history = full_history
date_history["Date"] = date_history["Date"].apply(lambda x: pd.Timestamp(year = x.year,month = x.month, day= x.day))

listeningYear = "2020"
if(date.today().year == int(listeningYear)):
    creationTime = datetime.fromtimestamp(os.path.getctime("./full_history.xlsx")).date()
    firstDayOfYear = date(int(listeningYear),1,1)
    nbDays = (creationTime - firstDayOfYear).days
else:
    nbDays = 365
date_history = date_history.loc[date_history["Date"].astype(str).str.find(listeningYear)!=-1]
print(nbDays)
print("Nombre total d'heures écoutées en "+listeningYear +" : ",date_history["Listening Time"].sum()/3600)
print("Nombres de minutes écoutées par jour : ",(date_history["Listening Time"].sum()/60)/nbDays )

'''Ecriture du fichier Excel d'output.'''
creationTime = datetime.fromtimestamp(os.path.getctime("./full_history.xlsx")).strftime("%d-%m-%y")
with pd.ExcelWriter("top_"+creationTime+".xlsx") as writer:
    title_top.to_excel(writer,sheet_name = "Top titres")
    album_top.to_excel(writer,sheet_name = "Top albums")
    album_ratio.to_excel(writer,sheet_name = "Top ratio albums")