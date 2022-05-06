# Projet P2 - Utilisez les bases de Python pour l'analyse de marché

## Sommaire
* Installation de l'environnement virtuel
* Installation des paquages avec le fichier requirement.txt
* Marche à suivre sur le fonctionnement des scripts

### Installation de l'environnement virtuel

Pour commencer il va falloir créer l'environnement virtuel. Copiez cette ligne dans la console Python. Ici nous créons un environnement virtuel <venv> nommé 'env'.
```
$ python -m venv env
```
Nous allons maintenant activer l'environnement virtuel avec la commande suivant : 
```
$ env/Scripts/activate.ps1
```
Votre environnement virtuel doit être installé.

### Installation des paquages avec le fichiers requirement.txt
Le fichier **requirement.txt** va installé automatiquement les paquages python nécessaires au bon fonctionnement des scripts. Pour utiliser celui-ci, ecrivez dans votre console Python la ligne suivante : 
```
$ pip install -r requirements.txt
```

Une fois vos essais terminés, vous pouvez désactiver l'environnement virtuel avec la commande : 
```
$ deactivate
```

En cas de problèmes référez-vous au lien suivant : [Les environnements virtuels](https://openclassrooms.com/fr/courses/6951236-mettez-en-place-votre-environnement-python/7014018-creez-votre-premier-environnement-virtuel).
### Marche à suivre sur le fonctionnement des scripts
   

#### scrap_article.py

Changez la variable "url_article" en haut du script, avec l'url d'un article de votre choix pour scrapper les informations d'un livre.
Sinon, par défaut, un lien est déjà saisi, vous pouvez simplement lancer le script et il s'exécutera.
Ces informations seront visibles dans la console mais aussi dans un fichier CSV qui sera créé dans le dossier '/scrap_CSV', se situant dans le même répertoire où est rangé le script.

#### scrap_categories.py

Changez la variable "url_category" en haut du script, avec l'url d'une catégorie de livre de votre choix pour scrapper tous les livres de la catégorie choisie.
Sinon, par défaut, un lien est déjà saisi, vous pouvez simplement lancer le script et il s'exécutera.
Vous pouvez suivre la progression du scrapping dans la console. Un fichier CSV sera créé avec le nom de la catégorie choisie listant toutes les informations de celle-ci.
Ce fichier sera créé dans le dossier "/scrap_CSV", se situant dans le même répertoire où est rangé le script.

#### scrap_site.py

Aucun changement d'URL n'est à faire comme le script scrap l'entièreté du site.
Vous pouvez suivre l'avancement du scrap dans la console. 
Des fichiers CSV seront créés tout au long de l'avancement du script, se situant dans le même répertoire où est rangé le script.

#### scrap_site_et_images.py

Aucun changement d'URL n'est à faire comme le script scrap l'entièreté du site.
Vous pouvez suivre l'avancement du scrap dans la console. 
Des fichiers CSV seront créés tout au long de l'avancement du script, se situant dans le même répertoire où est rangé le script.
Les images des différents livres parcourus seront stockées dans le dossier '/img_articles', se situant dans le même répertoire où est rangé le script.
Des sous-dossiers seront aussi créés, à l'intérieur de celui-ci, pour séparer les catégories de chaque image.
Les images sont numérotées et nommées comme leurs livres 

Une fois vos essais terminés, vous pouvez désactiver l'environnement virtuel avec la commande : 
```
$ deactivate
```