# Rapport d'installation et de tests : FasterLivePortrait et ComfyUI-LivePortraitKJ

## 1. Résumé

| Outil | Rôle | Résultat |
|---|---|---|
| FasterLivePortrait | Animer une photo avec une vidéo ou la webcam, accéléré avec TensorRT | Fonctionne, environ 14 images/s sur la vidéo d'exemple, mais le rendu ne correspond pas à ce que nous cherchons |
| ComfyUI-LivePortraitKJ | Animer une photo avec les mouvements de ma webcam, dans ComfyUI | Fonctionne en direct |

Les deux outils reposent sur LivePortrait (KwaiVGI). Ils ne changent pas le visage de la personne filmée : ils font bouger une photo fixe avec mes mouvements de tête, mes expressions et ma bouche. Je les ai testés les 11 et 12 novembre 2026 sur mon PC portable (RTX 4070 portable, 8 Go de VRAM), avant de retenir JoyAI-Video-Edit.

## 2. FasterLivePortrait

### 2.1 Présentation

[FasterLivePortrait](https://github.com/warmshao/FasterLivePortrait) est une version accélérée de LivePortrait. Il convertit les modèles ONNX en moteurs TensorRT optimisés pour la carte graphique. Il a trois modes : vidéo vers vidéo (`run.py`), interface web (`webui.bat`) et webcam en direct (`camera.bat`).

### 2.2 Installation (Windows)

Le README propose trois méthodes : un pack Windows tout-en-un, une image Docker ou une installation manuelle testée seulement sous Linux. J'ai pris le pack Windows, parce qu'il contient déjà Python, CUDA et TensorRT et évite de compiler TensorRT soi-même.

1. J'ai téléchargé `FasterLivePortrait-windows-20241228.zip` (9,35 Go) depuis Hugging Face. La connexion a coupé à 2,9 Go, alors j'ai repris le téléchargement avec `curl -C -` dans une boucle qui relance toute seule.
2. Le `tar` de Windows a refusé le zip, car il gère mal les zip de plus de 4 Go. Je l'ai décompressé avec le module `zipfile` de Python : 66 370 fichiers dans `D:\FasterLivePortrait-windows`. Le pack contient un `venv` Python 3.10 déjà prêt (torch 2.4 avec CUDA 12.1, TensorRT 9.0), les modèles ONNX et ffmpeg.
3. J'ai lancé `scripts\all_onnx2trt.bat`, qui a converti les 15 modèles en moteurs TensorRT en environ 50 minutes, sans erreur.

### 2.3 Tests

Vidéo d'exemple :

```
venv\python.exe run.py --src_image assets\examples\source\s10.jpg --dri_video assets\examples\driving\d14.mp4 --cfg configs\trt_infer.yaml
```

Chaque image prend environ 71 ms, soit à peu près 14 images par seconde. L'auteur annonce plus de 30 images par seconde, mais sur une RTX 3090 de bureau.

L'interface web se lance avec `webui.bat` et s'ouvre sur http://127.0.0.1:7890/ (et pas sur le port 9870 indiqué dans le README).

Webcam en direct, depuis le dossier `D:\FasterLivePortrait-windows` :

```
camera.bat --src_image C:\Users\robin\Downloads\test1.jpg --paste_back
```

`--paste_back` affiche la photo entière au lieu du visage recadré seul. Dans la fenêtre « Render », Q quitte le programme.

### 2.4 Problèmes rencontrés

| Problème | Cause | Correction |
|---|---|---|
| Plantage à la fin, au moment d'ajouter le son (`FileNotFoundError`) | Chemin relatif de ffmpeg mal lu par Windows | Chemin absolu dans `run.py`, `api.py` et `src\pipelines\gradio_live_portrait_pipeline.py` |
| Aucune image lue depuis la webcam (`inference median time: nan`) | Le pilote vidéo par défaut (MSMF) ouvre la webcam mais ne lit rien | Webcam ouverte avec `cv2.VideoCapture(0, cv2.CAP_DSHOW)` dans `run.py` |
| « no face » avec une photo dont le nom contient un espace | `camera.bat` ne mettait pas le chemin entre guillemets | Guillemets ajoutés dans `camera.bat`, photo renommée `test1.jpg` |

Il ne faut pas lancer `update.bat` : il fait un `git reset --hard` qui efface ces corrections.

### 2.5 Limites

Le logiciel fonctionne, mais le rendu ne correspond pas à notre objectif : il anime une photo au lieu de transformer la personne filmée. Les 14 images par seconde ont été mesurées sur la vidéo d'exemple, pas avec la webcam.

## 3. ComfyUI avec LivePortrait

### 3.1 Présentation

ComfyUI est une interface à nœuds pour faire tourner des modèles d'images et de vidéo en local. LivePortrait y anime une photo fixe avec mes mouvements captés par la webcam. J'ai utilisé le pack de nœuds [ComfyUI-LivePortraitKJ](https://github.com/kijai/ComfyUI-LivePortraitKJ) de kijai. Il affiche le résultat presque en temps réel, avec un retard annoncé d'environ 80 à 100 ms, et fournit un workflow d'exemple pour la webcam.

### 3.2 Installation (Windows)

1. J'ai installé Comfy Desktop depuis comfy.org, en choisissant la carte NVIDIA.
2. Dans le gestionnaire d'extensions de Comfy, j'ai installé `ComfyUI-LivePortraitKJ` et `ComfyUI-KJNodes` (ce dernier fournit le nœud de capture webcam), puis j'ai redémarré Comfy Desktop.
3. J'ai glissé dans la fenêtre le workflow d'exemple « realtime » du dossier `custom_nodes\ComfyUI-LivePortraitKJ\examples`. Quand des nœuds manquaient (en rouge), je les ai installés depuis la fenêtre « Missing nodes », puis j'ai redémarré.
4. Au premier lancement, les modèles se téléchargent seuls dans `models\liveportrait`.

La chaîne de nœuds : chargement des modèles, photo (`LoadImage`) et webcam (`Webcam Capture CV2`), détection du visage (`MediaPipeCropper`), `LivePortraitProcess`, puis `PreviewImage`.

### 3.3 Réglages utilisés

| Nœud | Réglage |
|---|---|
| `DownloadAndLoadLivePortraitModels` | précision `fp16` |
| `LivePortrait Load MediaPipeCropper` | device : CPU (à changer si l'image est saccadée) |
| `Webcam Capture CV2` | `cam_index` 0 (passer à 1 si l'image est noire ou vient de la mauvaise caméra) |
| `Screencap mss` | non relié, ignoré |
| Lancement | « Run (Instant) » à côté du bouton Run, pour que le traitement tourne en boucle |

J'ai choisi le détecteur MediaPipe, parce que la version InsightFace est compliquée à installer sous Windows. La photo doit être de face, bouche fermée, avec une expression neutre, un fond uni, les épaules visibles et aucun cheveu devant le visage.

### 3.4 Problème rencontré

Au premier lancement, le compteur « Total » est resté à 0 % pendant plus de 10 minutes. Le nœud de chargement des modèles les téléchargeait sans afficher de progression. Pour le vérifier, on regarde si la taille du dossier `models\liveportrait` augmente et on lit le panneau « Logs » de Comfy. Si rien ne bouge, on télécharge les modèles à la main.

## 4. Pourquoi nous ne les gardons pas

Les deux outils marchent sur mon PC, mais ils animent une photo au lieu de transformer la personne filmée. Pour notre démo, nous voulons modifier la vidéo en direct à partir d'une consigne, ce que fait JoyAI-Video-Edit (voir le [rapport sur les modèles vidéo](rapport-installations-modeles-Videos.md)). Les deux outils ont depuis été désinstallés de mon PC.

## Sources

- FasterLivePortrait : https://github.com/warmshao/FasterLivePortrait
- LivePortrait (KwaiVGI) : https://github.com/KwaiVGI/LivePortrait
- ComfyUI-LivePortraitKJ : https://github.com/kijai/ComfyUI-LivePortraitKJ
- Comfy Desktop : https://www.comfy.org
- Claude Code utilisé pour m'aider à installer et corriger FasterLivePortrait : https://claude.com/claude-code
