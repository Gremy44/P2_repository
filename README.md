                -------------------------------------------------------------
                ---- Marche à suivre pour faire fonctionner les scritps. ----
                -------------------------------------------------------------

    -----------------------
    ---- scrap_article ----
    -----------------------

Changez la variable "url_article" en haut du script, avec l'url d'un article de votre choix pour scrapper les information d'un livre.
Ces informations seront visible dans la console mais aussi dans un fichier CSV qui sera créé dans le dossier '/scrap_CSV',, se situant dans le même répertoire où est rangé le script.

    --------------------------
    ---- scrap_categories ----
    --------------------------

Changez la variable "url_category" en haut du script, avec l'url d'une categorie de livre de votre choix pour scrapper tous les livres de la catégorie choisie.
Vous pouvez suivre la progression du scrapping dans la console. Un fichier CSV sera créé avec le nom de la catégorie choisie listant toutes les informations de celle-ci.
Ce fichier sera créé dans le dossier "/scrap_CSV", se situant dans le même répertoire où est rangé le script.

    --------------------
    ---- scrap_site ----
    --------------------

Aucun changement d'URL n'est à faire comme le script scrap l'entièreté du site.
Vous pouvez suivre l'avancement du scrap dans la console. 
Des fichiers CSV seront créés tout au long de l'avancement du script, se situant dans le même répertoire où est rangé le script.

    ------------------------------
    ---- scrap_site_et_images ----
    ------------------------------

Aucun changement d'URL n'est à faire comme le script scrap l'entièreté du site.
Vous pouvez suivre l'avancement du scrap dans la console. 
Des fichiers CSV seront créés tout au long de l'avancement du script, se situant dans le même répertoire où est rangé le script.
Les images des différents livres parourus seront stockées dans le dossier '/img_articles', se situant dans le même répertoire où est rangé le script.
Des sous-dossiers seront aussi créés, à l'intérieur de celui-ci, pour séparer les catégories de chaques images.
Les images sont numérotés et nommé comme leur livres 
