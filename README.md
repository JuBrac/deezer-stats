Possibilités:
-

* Avoir la liste des morceaux les plus écoutés
* Avoir la liste des albums les plus écoutés
* Avoir la liste des albums les plus écoutés en ratio (Nb écoutes total/Nb morceaux de l'album)
* Avoir une calendar map (sur une ou plusieurs années) du nombre d'écoutes
* Avoir le nombre d'heures écoutés sur une année
* Avoir le nombre de minutes écoutés par jour sur une année

N.B : pour changer la taille de la liste de sortie, il faut changer TOP_NUMBER et listeningYear pour avoir les statistiques d'une année.


Instructions : 
-

Il vous faut votre historique d'écoute Deezer. Vous pouvez le demander par mail grâce au RGPD. Ils vous le fourniront normalement en 1 mois environ.

Renommez le "full_history.xlsx". Puis ensuite lorsque vous êtes dans le bon répertoire :
```bash
pip install july
python getAlbumJson.py
python parseHistory.py
```

En sortie vous aurez un fichier Excel avec plusieurs feuilles.

Fonctionnement : 
-

Le script getAlbumJson.py va effectuer des requêtes sur l'API Deezer pour dans un premier temps obtenir l'ID de tous les albums écoutées, puis dans un second temps obtenir le nombre de morceaux de chaque album. Il peut prendre du temps à s'exécuter si votre historique est long car il y aurait ainsi beaucoup de requêtes à effectuer.

Le second script parseHistory.py parcourt le fichier Excel et le fichier album_full.json (qui contient le nombre de morceaux des albums et leur pochette) pour faire les statistiques d'écoutes.