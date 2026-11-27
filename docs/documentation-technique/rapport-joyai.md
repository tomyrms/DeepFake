# Rapport JoyAI

## 1. Résumé

J'ai installé JoyAI-Video-Edit 1.1 sur la RTX 5090 que nous louons chez SwissGPU, puis je l'ai testé avec ma webcam. Le modèle fonctionne : il remplace la personne filmée en suivant les mouvements de la tête, à 840 × 480.

Les résultats sont moins bons que ce qu'annoncent les auteurs :

- environ 10 images/s pendant l'édition au lieu de 24 ;
- une bouche mal rendue quand on parle ;
- des yeux qui suivent mal le regard ;
- une dérive après 15 à 20 secondes : le fond tourne, la caméra semble bouger, le visage change.

Les meilleurs résultats viennent de consignes courtes, d'une webcam fixe, d'un fond uni et d'une relance régulière de l'édition.

| Élément           | Valeur                                                          |
| ----------------- | --------------------------------------------------------------- |
| Modèle            | JoyAI-Video-Edit 1.1 (DiT de 16 milliards de paramètres)        |
| Serveur           | SwissGPU, Ubuntu, RTX 5090 de 32 Go                             |
| Résolution testée | 840 × 480                                                       |
| Mémoire utilisée  | 23,8 Gio sur 31,4 une fois le modèle chargé                     |
| Temps par bloc    | 0,44 s avant l'édition, 0,77 s pendant l'édition (8 images)     |
| Débit pendant l'édition | environ 10 images/s                                       |

## 2. Fonctionnement de JoyAI-Video-Edit

JoyAI-Video-Edit est un modèle open source de l'entreprise JD. Il reçoit la vidéo de la webcam et une consigne écrite en anglais, et il renvoie la vidéo modifiée presque en direct. Il est composé de trois parties :

- un **DiT** de 16 milliards de paramètres, qui génère les images (fichier `joyai_video_edit_dit_1101_face++.pth`) ;
- **MiMo-VL-7B**, qui lit la consigne et l'image de référence ;
- un **VAE**, qui compresse et décompresse les images.

Le serveur traite la vidéo par **blocs de 8 images**. La page web envoie les images de la webcam par WebSocket, sur le port 8080, et affiche le résultat. Chaque bloc s'appuie sur les blocs déjà générés pour rester cohérent.

## 3. Connexion au serveur

SwissGPU nous prête un serveur Ubuntu avec une RTX 5090 de 32 Go et les pilotes NVIDIA déjà installés. On s'y connecte en SSH par mot de passe, avec la commande fournie par SwissGPU. L'adresse et le port ne sont pas notés ici, car le dépôt est public.

J'ajoute à cette commande un tunnel vers le port 8080 avec l'option `-L 8080:localhost:8080`. La page de JoyAI s'ouvre alors à l'adresse `http://localhost:8080` sur mon PC. Ce tunnel est nécessaire : le navigateur n'autorise la webcam que sur une page en `https` ou en `localhost`.

Je travaille dans `tmux` pour que l'installation et le serveur continuent si la connexion coupe.

## 4. Installation

J'ai suivi le [guide de déploiement](https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md) de JoyAI.

1. Installer Miniconda et créer l'environnement `joyai-video-edit` avec Python 3.10.
2. Installer PyTorch 2.9.1 pour CUDA 12.8, puis le compilateur CUDA 12.8 (`nvcc`) depuis conda-forge.
3. Compiler SageAttention 2.2.0 pour la RTX 5090, avec le correctif fourni par JoyAI et `TORCH_CUDA_ARCH_LIST=12.0`. FlashAttention 4 n'est pas compatible avec cette carte.
4. Compiler les noyaux `joyomni_ops` avec CUTLASS.
5. Télécharger les poids sur Hugging Face : le DiT de la version 1.1 (31 Go), le VAE (1,5 Go) et MiMo-VL-7B (16 Go). Le modèle Qwen qui améliore les consignes n'est pas utilisé avec le profil RTX 5090.

### Problèmes rencontrés

| Problème                                              | Cause                                                                      | Solution                                                                                                                   |
| ----------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `CondaToSNonInteractiveError`                         | Conda demande d'accepter les conditions d'Anaconda pour ses canaux         | `conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main`, puis la même commande pour `/pkgs/r` |
| `pip` ou `hf` introuvable                             | Nouveau terminal, l'environnement n'est pas activé                         | `source ~/miniconda3/etc/profile.d/conda.sh`, puis `conda activate joyai-video-edit`                                       |
| `diffusers` ne démarre plus                           | `huggingface_hub` mis à jour en version 2                                  | Revenir à la version 1.33.0 : `pip install "huggingface_hub==1.33.0"`                                                      |
| Téléchargement d'un seul fichier au lieu de plusieurs | Plusieurs motifs après un seul `--include`                                 | Répéter `--include` devant chaque motif                                                                                    |
| Le serveur s'arrête juste après le démarrage          | Un Ctrl+C pendant le chargement est appliqué une fois le démarrage terminé | Relancer et ne pas appuyer sur Ctrl+C pendant le chargement                                                                |

Le premier démarrage compile pendant plusieurs minutes pour chaque résolution. Le résultat est gardé en cache dans `deploy/deps/cache_rtx5090`, ce qui accélère les démarrages suivants.

## 5. Lancement

J'ai écrit le script `~/start-joyai.sh` pour lancer le serveur avec le profil RTX 5090 et choisir une résolution :

```bash
#!/bin/bash
# Utilisation : ~/start-joyai.sh [qualite|equilibre|rapide|720p]
source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate joyai-video-edit
cd ~/JoyAI-Video-Edit
PROFIL=${1:-equilibre}
case "$PROFIL" in
  qualite)   W=840;  H=480; FPS=24 ;;
  equilibre) W=840;  H=480; FPS=12 ;;
  rapide)    W=672;  H=384; FPS=16 ;;
  720p)      W=1248; H=720; FPS=8  ;;
  *) echo "Profil inconnu : $PROFIL (qualite, equilibre, rapide ou 720p)"; exit 1 ;;
esac
echo "Profil $PROFIL : ${W}x${H} a ${FPS} images/s"
mkdir -p ~/joyai-logs
LOG=~/joyai-logs/$(date +%Y%m%d-%H%M)-$PROFIL.log
JOYOMNI_WIDTH=$W JOYOMNI_HEIGHT=$H JOYOMNI_FPS=$FPS \
JOYOMNI_CACHE_ROOT=$PWD/deploy/deps/cache_rtx5090 \
JOYOMNI_FA4_ATTN=0 JOYOMNI_SAGE_ATTN=1 JOYOMNI_FP8_FAST_ACCUM=1 JOYOMNI_LOW_VRAM=1 \
JOYOMNI_PE_BACKEND=none \
bash deploy/run_server.sh 2>&1 | tee "$LOG"
```

| Variable | Rôle |
| -------- | ---- |
| `JOYOMNI_FA4_ATTN=0` | Désactive FlashAttention 4, incompatible avec la RTX 5090 |
| `JOYOMNI_SAGE_ATTN=1` | Utilise SageAttention à la place |
| `JOYOMNI_FP8_FAST_ACCUM=1` | Calculs en FP8, plus rapides |
| `JOYOMNI_LOW_VRAM=1` | Mode basse mémoire pour tenir dans 32 Go |
| `JOYOMNI_PE_BACKEND=none` | Pas d'amélioration automatique des consignes |
| `JOYOMNI_WIDTH`, `JOYOMNI_HEIGHT`, `JOYOMNI_FPS` | Résolution et débit (840 × 480 à 24 images/s par défaut) |

Le serveur est prêt quand le journal affiche `Application startup complete`. On l'arrête avec Ctrl+C. Chaque lancement écrit un journal dans `~/joyai-logs`.

## 6. Utilisation de la page web

1. Ouvrir `http://localhost:8080` avec le tunnel SSH actif et autoriser la webcam.
2. Écrire la consigne en anglais dans la zone de texte.
3. Pour utiliser un visage précis, ajouter une photo avec le **＋** et la citer dans la consigne avec « Image 1 ».
4. Cliquer sur **↑** pour lancer l'édition. Sans ce clic, la page affiche seulement la webcam.

L'édition démarre une fois qu'un visage est détecté. Le journal affiche alors `FACE-GATE passed`.

## 7. Tests

### 7.1 Remplacement de la tête avec une photo

Avec l'accord de Tomas, j'ai utilisé sa photo comme image de référence. Le modèle régénère bien la tête et suit ses mouvements, mais il reprend l'expression de la photo et gère mal la bouche : quand j'ouvre la bouche, celle de l'image générée reste presque fermée ou se déforme.

La photo de référence donne de meilleurs résultats si elle respecte ces points :

- de face, la tête droite, les deux oreilles visibles ;
- expression neutre, sans sourire, la bouche fermée ou à peine entrouverte ;
- lumière douce et égale, sans ombre forte ;
- sans lunettes ni cheveux devant les yeux ;
- tête et épaules, sur un fond simple, avec une image nette.

### 7.2 Personne inventée, sans photo

Sans image de référence, il faut demander clairement une autre personne. Sinon, le modèle garde mon visage et change seulement les vêtements. La consigne qui a donné le meilleur résultat pour un employé de banque :

```
Replace the person in the video with a completely different man: a bank employee in his forties, short brown hair, clean-shaven, sitting in his office, wearing a black headset with a microphone, navy suit, white shirt, tie. Behind him, a plain office wall with one framed painting hanging on it. Static webcam, the camera and background never move. Keep the head and eyes motion from the video. Realistic webcam image.
```

Version avec la photo de référence :

```
Replace the person in the video with the person from Image 1, keeping the face from Image 1. The person is a bank employee sitting in the office, wearing a black headset with a microphone, navy suit, white shirt, tie. Behind, a plain office wall with one framed painting hanging on it. Static webcam, the camera and background never move. Keep the head and eyes motion from the video. Realistic webcam image.
```

Je n'utilise pas de nom ni de logo de vraie banque. Une vidéo avec la marque d'une vraie banque pourrait servir à une arnaque.

### 7.3 Ce que j'ai appris sur les consignes

- **Mettre l'essentiel au début.** Le modèle suit mieux ce qui vient en premier.
- **Rester court.** Avec une longue consigne, le modèle lâche une partie des demandes au fil du temps.
- **Demander une caméra fixe**, par exemple « Static webcam, the camera and background never move ».
- **Limiter le décor** : un mur uni et un seul tableau bougent moins qu'un bureau rempli d'objets ou des personnes qui passent derrière.
- **Bouche fermée** : la demander (« Keep the mouth closed at all times ») cache les défauts de la bouche quand on ne parle pas.
- **Yeux** : demander qu'ils suivent la vidéo et clignent, et décrire « clear visible eyes ».

## 8. Problèmes observés

### 8.1 Débit et retard

Pendant l'édition, le serveur traite environ 10 images/s alors que la page en envoie 24. Les images s'accumulent dans la file d'attente (32 images au maximum) et le retard augmente. Le retard vient de quatre sources : le temps de remplir un bloc de 8 images, le calcul, la file d'attente et le réseau.

Les profils `equilibre` (840 × 480 à 12 images/s) et `rapide` (672 × 384 à 16 images/s) du script servent à envoyer moins d'images que ce que le serveur peut traiter.

### 8.2 Bouche et yeux

La bouche et les yeux sont les parties les plus difficiles pour le modèle. À 840 × 480, ils font peu de pixels, et un mouvement de moins d'un tiers de seconde tient dans un seul bloc de 8 images. Ce qui aide :

- se rapprocher de la webcam ;
- éclairer le visage de face ;
- faire des mouvements lents et un peu exagérés ;
- utiliser une photo de référence neutre.

### 8.3 Dérive après 15 à 20 secondes

Après 15 à 20 secondes, le modèle s'éloigne de la vidéo : le fond tourne, la caméra semble bouger et le visage change. Chaque bloc s'appuie sur les précédents, donc les petites erreurs s'accumulent. C'est une limite des modèles vidéo qui génèrent en continu.

Ce qui limite la dérive :

- relancer l'édition avec **↑** toutes les 10 à 15 secondes, sans changer la consigne ;
- utiliser le profil `equilibre` pour éviter que la file d'attente se remplisse ;
- poser la webcam sur un support fixe, devant un fond uni, avec une lumière stable ;
- garder une consigne courte.

Je n'ai pas encore vérifié dans le code de JoyAI s'il existe un réglage qui limite la mémoire des blocs précédents.

## 9. Combinaison avec Deep-Live-Cam et OBS

Deep-Live-Cam suit beaucoup mieux la bouche que JoyAI. Il faut le placer **avant** JoyAI. Placé après, il recopierait la bouche fermée de la sortie de JoyAI.

```
Webcam → Deep-Live-Cam (visage, bouche) → OBS, caméra virtuelle
       → page JoyAI (vêtements, décor) → OBS, projecteur plein écran
```

1. Lancer Deep-Live-Cam sur le PC, avec la photo source et la vraie webcam.
2. Dans OBS, créer une scène **DLC** avec une capture de la fenêtre de Deep-Live-Cam.
3. Régler la caméra virtuelle sur **Type de sortie : Scène**, scène **DLC**, pour éviter une boucle, puis la démarrer.
4. Dans Chrome, choisir **OBS Virtual Camera** pour la page JoyAI. Ne pas ajouter d'image de référence, et demander dans la consigne de garder le visage et la bouche.
5. Dans OBS, créer une scène **Écran** avec une capture de Chrome recadrée sur la sortie de JoyAI, puis l'ajuster à l'écran (Ctrl+F).
6. Clic droit sur la scène **Écran**, puis **Projecteur plein écran (scène)** sur le grand écran.

Cette chaîne additionne les retards de Deep-Live-Cam, de JoyAI et d'OBS. Je ne l'ai pas encore mesurée.

## 10. Suite du travail

- Comparer les profils `qualite`, `equilibre` et `rapide` : temps par bloc, mémoire et rendu du visage.
- Essayer le profil `720p` pour voir s'il tient dans 32 Go. Ce test servira à décider si nous demandons une RTX PRO 6000 pour les portes ouvertes du 15 janvier 2027.
- Vérifier si la page web suit le débit fixé par le serveur.
- Mesurer le retard entre la webcam et l'image modifiée depuis le réseau de l'école, en filmant un chronomètre.
- Tester la chaîne Deep-Live-Cam, JoyAI et OBS, et mesurer le retard ajouté.

Ces tâches sont suivies dans les issues [#73](https://github.com/tomyrms/DeepFake/issues/73), [#74](https://github.com/tomyrms/DeepFake/issues/74), [#75](https://github.com/tomyrms/DeepFake/issues/75) et [#76](https://github.com/tomyrms/DeepFake/issues/76).

## Sources

- [Dépôt GitHub de JoyAI-Video-Edit](https://github.com/jd-opensource/JoyAI-Video-Edit)
- [Guide de déploiement de JoyAI-Video-Edit](https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md)
- [Rapport sur les choix techniques](rapport-choix-techniques.md)
- [Rapport d'installation des modèles vidéo](rapport-installations-modeles-Videos.md)

[Retour à la documentation technique](README.md)
