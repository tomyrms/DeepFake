# Semaine du 23 au 29 novembre 2026

Semaine en cours.

## Mardi 24 novembre

### Tomas :
SwissGPU nous a donné les détails du serveur. Il tourne sous Ubuntu, avec un accès SSH, les droits administrateur et les pilotes NVIDIA déjà installés. Ils préfèrent nous prêter un serveur plusieurs jours d’affilée plutôt que de répartir les 10 heures, et ils ne gardent pas nos données une fois le serveur attribué à un autre client.

Je leur ai demandé une RTX 5090 du mercredi 25 novembre au vendredi 4 décembre, ou sinon à partir du mardi 1er décembre. Pour les portes ouvertes du 15 janvier 2027, de 16 h à 21 h, nous aimerions une RTX PRO 6000 Blackwell pour faire tourner le modèle dans une meilleure résolution. Nous attendons leur réponse.

### Robin : 
j’ai mis à jour le rapport d’installation des modèles vidéo. JoyAI-Video-Edit y remplace ComfyUI avec LivePortrait : le rapport présente sa démo sur Hugging Face et le désigne comme la solution retenue pour l’installation en local.

## Mercredi 25 novembre

### Tomas : 
j’ai testé seed-vc-realtime et MeanVC2 au micro, avec un extrait de 27 secondes de la voix de Kylian Mbappé. Les deux fonctionnent, mais le résultat n’est pas convaincant et seed-vc coupe beaucoup. Ce sont des modèles zero-shot, qui imitent une voix sans entraînement.

J’ai donc retenu RVC v2, où l’on entraîne un modèle sur la voix cible. À partir d’une interview de 53 minutes, j’ai gardé uniquement sa voix, soit 42 minutes et demie. Pour cela, j’ai transcrit l’interview avec Whisper, puis séparé les deux voix avec SpeechBrain.

J’ai installé Applio 3.7.2 pour l’entraînement et la conversion en temps réel. L’entraînement a tourné sur la RTX 4070 de 14 h 45 à 16 h 36, jusqu’à l’époque 55, à environ 1 min 10 par époque. À l’époque 10, la voix ne ressemblait pas encore à la sienne. À l’époque 50, dernier modèle sauvegardé, elle lui ressemble. Il me reste à comparer les époques 20 et 30.

### Robin : 
je me suis connecté en SSH au serveur de SwissGPU et j’ai ajouté un tunnel vers le port 8080, pour ouvrir la page de JoyAI à l’adresse `http://localhost:8080` sur mon PC. Le navigateur n’autorise la webcam que sur une page en `localhost` ou en `https`, donc ce tunnel est nécessaire. 

J’ai ensuite installé JoyAI-Video-Edit sur la RTX 5090 et je l’ai testé avec ma webcam. Le modèle remplace bien la personne filmée mais il gère mal la bouche et les yeux, et l’image dérive après 15 à 20 secondes. J’ai réinstallé Deep-Live-Cam sur mon PC et préparé deux scènes OBS pour enchaîner Deep-Live-Cam et JoyAI et afficher le résultat en plein écran. La bouche ne s’ouvre toujours pas bien avec cette combinaison, je dois encore tester chaque outil séparément. Mais nous allons certainement utilisé seulement JoyAI. Je suis en train de rédiger le rapport JoyAI, sur l’installation et les tests de JoyAI-Video-Edit. J’ai aussi créé les issues de connexion, d’installation, de test et d’optimisation.

## Vendredi 27 novembre

### Nous deux : 
Lors du daily avec M. Gomez, nous avons parlé des limites du modèle sur la RTX 5090 : il tourne seulement en 840 × 480. Pour les portes ouvertes, nous allons axer la présentation sur la sensibilisation aux deepfakes et à leurs dangers. Nous avons confirmé que nous garderions la RTX 5090, avec ses limites, sans chercher une carte plus puissante. Nous présenterons deux solutions : JoyAI-Video-Edit sur la RTX 5090, et Deep-Live-Cam sur notre PC portable. Le public verra ainsi ce qu’on peut faire avec une carte graphique moyenne et avec une carte puissante. Nous avons aussi parlé du frontend pour les portes ouvertes : il doit être très simple à utiliser pour les visiteurs, et assez impressionnant pour attirer leur attention.

### Tomas : 
il a dû partir juste après le daily.

### Robin : 
j’ai rédigé un mail à SwissGPU pour demander une semaine de plus sur le serveur et confirmer le serveur avec la RTX 5090 pour les portes ouvertes. Je suis en attente d'une réponse. J’ai aussi rédigé le journal de travail de la semaine et je l’ai envoyé. Et pour finir, j’ai continué les tests de JoyAI-Video-Edit et la rédaction du rapport JoyAI.

## Conclusion de la semaine

JoyAI-Video-Edit tourne maintenant sur la RTX 5090 de SwissGPU. Il remplace bien la personne filmée, mais il est limité à 840 × 480, gère mal la bouche et les yeux et dérive après 15 à 20 secondes. Côté voix, RVC v2 donne de meilleurs résultats que les modèles zero-shot, et le modèle entraîné commence à ressembler à la voix cible. Avec M. Gomez, nous avons décidé de garder la RTX 5090 pour les portes ouvertes et d’axer la présentation sur les dangers des deepfakes, en comparant JoyAI-Video-Edit et Deep-Live-Cam sur notre PC portable. Il reste à améliorer le rendu de JoyAI, à finir l’entraînement de la voix, à synchroniser la voix et la vidéo, à concevoir le frontend et à attendre la réponse de SwissGPU.

[Retour au journal](README.md)

