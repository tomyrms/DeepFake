# FasterLivePortrait — notes des 11 et 12 novembre 2026

Essais du pack Windows de [FasterLivePortrait](https://github.com/warmshao/FasterLivePortrait) sur une RTX 4070, pour animer une photo avec la webcam.

## Installation

Nous avons choisi le pack Windows pour ses dépendances incluses : Python 3.10, PyTorch 2.4 avec CUDA 12.1 et TensorRT 9.0. Le GPU était détecté et `scripts\all_onnx2trt.bat` a converti les **15 modèles ONNX en moteurs TensorRT**.

| Problème | Correction appliquée |
|---|---|
| Téléchargement interrompu du pack de 9,35 Go | Reprise avec `curl -C -`. |
| Extraction refusée par `tar` sous Windows | Extraction avec le module Python `zipfile`. |
| FFmpeg introuvable à l’ajout du son | Chemin absolu vers le FFmpeg fourni dans `run.py`, `api.py` et `src\pipelines\gradio_live_portrait_pipeline.py`. |
| Webcam fermée sans traiter d’image | Ouverture avec `cv2.VideoCapture(0, cv2.CAP_DSHOW)` dans `run.py`. |
| Chemin de photo coupé aux espaces | Guillemets autour de `!src_image!` dans `camera.bat`. |

## Lancement et résultats

Depuis le dossier du pack, l’essai vidéo utilise :

```bat
venv\python.exe run.py --src_image assets\examples\source\s10.jpg --dri_video assets\examples\driving\d14.mp4 --cfg configs\trt_infer.yaml
```

Après correction de FFmpeg, la vidéo avec son a été générée. Le relevé de **71 ms par image, soit environ 14 images/s** (`1 000 ÷ 71`), concerne cette vidéo d’exemple, pas le débit ni le délai complet de la webcam.

L’interface web se lance avec `webui.bat` et était accessible sur [le port local 7890](http://127.0.0.1:7890/).

Pour la webcam, depuis une invite de commandes ouverte dans le dossier du pack :

```bat
camera.bat --src_image "%USERPROFILE%\Pictures\test1.jpg" --paste_back
```

Le script utilise l’environnement Python fourni. L’option `--paste_back` affiche la photo entière ; elle ne génère pas de nouveaux cheveux.

Les trois modes ont été testés, mais **le résultat ne correspond pas à notre objectif**. Aucun débit webcam n’a été consigné.

Les corrections locales doivent être sauvegardées avant une mise à jour : le `git reset --hard` de `update.bat` peut les effacer.

[Retour au bilan de la semaine](2026-W46.md) · [Index du journal](README.md)
