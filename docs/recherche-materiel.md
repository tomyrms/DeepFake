# Outils et matériel pour la démonstration d’IA locale

Recherche préliminaire du **10 novembre 2026**, pour le projet scolaire de Tomas et Robin. Nous préparons une démonstration en direct par webcam pour les portes ouvertes, envisagées le **15 janvier 2027**, date à confirmer. **Le budget reste à déterminer.**

> **Évolution au 13 novembre 2026 :** Deep-Live-Cam a été testé sur notre PC. Le résultat était trop lent, saccadé et de qualité insuffisante ; il remplaçait le visage sans transformer les cheveux ni le reste de la tête. Nous recherchons une solution de transformation générative de la tête entière et avons choisi de tester une **RTX 5090 de 32 Go de VRAM chez SwissGPU**. Le [rapport illustré](rapport-choix-techniques.md) présente ces résultats et ce choix. Le reste de cette note conserve la recherche initiale du 10 novembre.

## Point de départ

Le PC disponible possède un **Intel Core i7-13700HX**, une **NVIDIA GeForce RTX 4070 Laptop avec environ 8 Go de VRAM** et environ **32 Go de RAM**, d’après l’inventaire réalisé. Il servira de première machine d’essai. Aucun débit ni délai d’affichage n’a encore été mesuré : sa capacité à assurer la démonstration en direct reste à vérifier.

Robin a depuis terminé une première installation de **Deep-Live-Cam sur son PC**, également équipé d’une RTX 4070 selon son journal. Il y rapporte la présence des deux modèles ONNX et la détection du GPU par PyTorch et ONNX Runtime. Les autres caractéristiques du PC inventorié ci-dessus ne sont pas attribuées à cette machine sans confirmation. Le premier lancement avec webcam et les mesures de performance restent à faire. Voir le [journal du 10 novembre](journal/2026-11-10.md).

## Deux outils à comparer

| Outil | Intérêt pour le projet | Matériel et licences publiés |
|---|---|---|
| **FaceFusion** | Mode webcam documenté, en plus du traitement de fichiers vidéo. | La FAQ annonce **8 Go de VRAM au minimum et 12 Go ou plus conseillés**. Le logiciel est distribué sous **OpenRAIL-AS** ; les modèles ont leurs propres licences. [Webcam](https://docs.facefusion.io/usage/deepfake-webcam), [FAQ matériel](https://docs.facefusion.io/faq), [licences](https://docs.facefusion.io/introduction/licenses). |
| **Deep-Live-Cam** | Mode webcam et accélération NVIDIA CUDA documentés. | Le code du dépôt est sous **AGPL-3.0**. Le site recommande **6 Go de VRAM ou plus pour ses éditions préconfigurées** ; ce chiffre ne garantit pas les performances de la version installée depuis les sources. [Dépôt officiel](https://github.com/hacksider/Deep-Live-Cam), [recommandations du site](https://deeplivecam.net/). |

Nous privilégions les outils ouverts et l’installation depuis les sources, approche retenue pour le premier essai de Robin. La présence de sources accessibles ne suffit pas à conclure que toutes les licences sont équivalentes : FaceFusion doit notamment être évalué selon sa licence OpenRAIL-AS. Ses installateurs payants sont facultatifs. [Site FaceFusion](https://facefusion.io/), [licences FaceFusion](https://docs.facefusion.io/introduction/licenses).

Les **modèles doivent être examinés séparément du logiciel**. InsightFace distingue son code sous MIT des données et modèles annoncés pour la recherche non commerciale, et fournit des indications spécifiques de licence pour certains modèles. Le choix devra donc porter sur un outil **et** des modèles compatibles avec la démonstration envisagée. [Conditions InsightFace](https://github.com/deepinsight/insightface#license).

## Configuration à étudier pour un prêt

Une piste de comparaison serait un GPU NVIDIA compatible avec l’environnement CUDA retenu, **12 à 16 Go de VRAM**, **32 Go de RAM** et un **SSD de 1 To**, avec une marge pour les modèles et fichiers temporaires.

Cette configuration est une **estimation de projet**, pas un minimum officiel commun aux deux outils. Aucun GPU ni prix n’est arrêté. La VRAM seule ne garantit pas la fluidité : le calcul disponible, les réglages, le refroidissement et l’affichage comptent aussi. La priorité est d’essayer le matériel disponible avant de proposer un achat.

## Essai prévu

Pour comparer le PC actuel à un éventuel prêt, nous utiliserons le même scénario et les mêmes réglages :

1. Commencer avec un visage consenti, une image en **720p** et une **cible proposée de 25 images/s**, à confirmer après les premiers essais. Le caractère synthétique sera annoncé.
2. Vérifier que le calcul utilise le GPU et consigner les versions du logiciel, des dépendances et du modèle.
3. Faire un essai de **10 à 15 minutes**, sur secteur, avec la webcam et l’affichage prévus. Relever le débit, les ralentissements, le délai entre le mouvement et son affichage, ainsi que les pics de VRAM et de RAM.
4. Tester plusieurs démarrages, les variations de lumière et les interruptions de webcam. Comparer séparément les options d’amélioration d’image. Vérifier aussi le fonctionnement local une fois les ressources nécessaires préparées.
5. Après validation du prototype, préparer une courte vidéo de secours. Une éventuelle demande d’achat devra s’appuyer sur une limite mesurée et sur les possibilités de prêt de l’école.

Ce protocole est une proposition ; **l’essai complet n’a pas encore été exécuté**. Les contrôles de détection GPU rapportés par Robin constituent une première étape, sans certifier la compatibilité de toute la chaîne de traitement. Les documents techniques des outils serviront à ajuster les réglages, notamment la [documentation de Deep-Live-Cam](https://github.com/hacksider/Deep-Live-Cam) et sa [FAQ](https://deeplivecam.net/index.php/faq).

## Brouillon de demande à l’école — non envoyé

> Objet : prêt d’un PC pour notre démonstration d’IA locale
>
> Bonjour,
>
> Pour notre projet scolaire, nous préparons une démonstration d’IA locale en direct par webcam. Les portes ouvertes seraient le 15 janvier 2027 ; pourriez-vous confirmer cette date ?
>
> Le PC disponible possède une RTX 4070 Laptop avec environ 8 Go de mémoire graphique et 32 Go de RAM. Nous allons d’abord mesurer ses performances. Pourriez-vous nous indiquer quels PC seraient disponibles en prêt, avec leurs caractéristiques : processeur, GPU exact et VRAM, RAM, stockage et système d’exploitation ?
>
> Une machine avec 12 à 16 Go de VRAM, 32 Go de RAM et un SSD de 1 To serait une piste de comparaison à valider par un essai. Le budget reste à déterminer. Nous privilégions les outils ouverts et vérifierons les licences des modèles retenus.
>
> Serait-il possible de prévoir un prêt pour les essais et la présentation, avec une webcam, un écran ou projecteur et les droits d’installation nécessaires ? Nous pourrons ensuite transmettre nos résultats et une éventuelle demande chiffrée.
>
> Merci,
> Tomas et Robin

Aucun achat de matériel n’a été réalisé. Robin rapporte le téléchargement des modèles et la fin de l’installation, mais aucun essai d’inférence avec la webcam, relevé de performances ou test hors ligne n’est encore documenté. Cette note sera mise à jour avec ces résultats.

[Retour au projet](../README.md) · [Journal](journal/README.md)
