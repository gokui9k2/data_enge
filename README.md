### Introduction
Pour ce projet, nous avons décidé de scraper le site de l'UFC car nous sommes passionnés par les sports de combat. Voici l'URL concernée : "http://ufcstats.com/statistics/events/completed".

### Scrapy
Nous avons commencé par scraper les données des combattants, c'est-à-dire toutes leurs caractéristiques. Pour cela, nous avons utilisé le code suivant :

- Photo du code Scrapy d'Andy
  ![Texte alternatif](Image/Interface.png)

- Photo du code Scrapy de Cyril
  ![Texte alternatif](Image/Interface.png)

Dans ces scripts, nous parcourons plusieurs pages et scrapons les données qui nous intéressent. Ensuite, nous procédons à un nettoyage des données pour les rendre plus lisibles et plus simples à analyser. À chaque appel récursif, nous intégrons les données dans notre base de données MongoDB, même si, après analyse, cette solution ne semble pas la plus adaptée en raison de sa complexité.

Nous avons effectué plusieurs améliorations dans notre script Scrapy. Dans le `DC_spider`, nous avions initialement effectué un nettoyage de données trop agressif, ce qui a entraîné une perte significative de données. Après avoir allégé cette étape, nous sommes passés de 3500 lignes et 135 colonnes à 6500 lignes, et après quelques améliorations, à 7133 lignes.

Pour améliorer notre script Scrapy, nous avons pris plusieurs mesures :
1. Nous avons mis en place un bulk pour l'intégration des données dans MongoDB, ce qui a réduit le temps de traitement de 2.89 secondes à 2.74 secondes par page scrapée.
2. Nous avons ajusté les paramètres `CONCURRENT_REQUESTS` et `CONCURRENT_REQUESTS_PER_DOMAIN` et trouvé que les valeurs 32 et 5, respectivement, offraient les meilleurs résultats, réduisant le temps de traitement à 1.77 secondes.
3. Nous avons introduit une fonction `safe_get` pour gérer les cas où un combattant est mis KO, évitant ainsi des erreurs dues à l'absence de données. Cependant, cette modification n'a pas amélioré les performances comme espéré, et le temps de traitement est remonté à 2.60 secondes.

Faute de temps, nous n'avons pas pu intégrer la version améliorée du script à notre projet en raison d'une petite erreur dans le code qui affectait le bulk, nous laissant avec un dataset de 7222 lignes et une colonne.

### Nettoyage des données
Nous avons commencé par nettoyer les données en retirant tous les caractères spéciaux. La première étape consistait à nettoyer la colonne `class` pour la remplacer par des catégories, ce qui s'est avéré relativement simple car les données étaient bien structurées.

Le plus gros du travail a concerné le dataset sur les caractéristiques des combattants, qui était moins bien structuré. Beaucoup de valeurs manquantes étaient dues à une mauvaise documentation sur le site de l'UFC. Nous avons créé une nouvelle variable `class` pour affiner notre nettoyage et, grâce au premier dataset, une variable `gender` pour plus de précision.

Pour gérer les données manquantes sur la taille et l'allonge, nous avons remplacé les valeurs manquantes en utilisant la corrélation entre ces deux mesures. Face à la difficulté de remplacer précisément le poids, nous avons opté pour un modèle de machine learning avec une précision de 70%, ce qui est satisfaisant étant donné que l'optimisation maximale n'était pas l'objectif principal de ce projet.






























