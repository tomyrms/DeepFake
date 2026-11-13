# Notes techniques de la semaine 46

**Robin — travail du 12 novembre 2026.** Ces notes décrivent l’installation utilisée pour animer une photo avec la webcam dans Comfy Desktop et ComfyUI-LivePortraitKJ. Les versions relevées dans le compte rendu sont Python 3.13 et PyTorch 2.12 ; les solutions ci-dessous correspondent à cette installation.

## Blocages et solutions appliquées

Les heures sont des repères consignés pendant le travail, pas un relevé de durée de séance.

| Heure notée | Problème rencontré | Solution ou constat |
|---|---|---|
| 13 h 54 | Aucun bouton « Manager » visible. | J’ai trouvé **Manage Extensions** dans le menu principal, sous le logo « C ». |
| 14 h 21 | Progression bloquée à 0 % pendant environ dix minutes. | Le premier lancement téléchargeait les modèles sans afficher de progression. |
| 14 h 25 | `motion_extractor.safetensors` absent après un téléchargement interrompu. | J’ai supprimé le dossier `models\liveportrait`, puis relancé le téléchargement des modèles. |
| 14 h 42 | Erreur `No module named 'mediapipe.framework'`. | J’ai remplacé MediaPipeCropper par **LivePortrait Load FaceAlignmentCropper**, avec `blazeface`, `cuda` et `fp16`. |
| 14 h 49 | Erreur `Weights only load failed` sur `landmark_model.pth`. | J’ai réglé `landmarkrunner_device` sur **CPU** ; ce chemin utilise `landmark.onnx`. |
| 14 h 50 | Erreur `No module named 'skimage'`. | J’ai installé `scikit-image`, `numba` et `scipy` dans l’environnement Python de Comfy. |
| 15 h 01 | Erreur `No module named 'comfyui-liveportraitkj'` au chargement de `blazeface`. | J’ai corrigé l’import dans `face_alignment\api.py`, à la ligne 79 de cette installation, avec `'.detection.' + face_detector` et `package=__package__`. L’original est conservé dans `api_ancien.py` ; une mise à jour du pack peut écraser cette correction locale. |
| 15 h 10 | L’aperçu produisait une photo par clic. | J’ai activé **Run (Instant)** pour relancer le workflow en boucle. |

## Réglages du workflow utilisé

J’ai repris l’exemple « realtime » de ComfyUI-LivePortraitKJ et remplacé son détecteur MediaPipe par FaceAlignmentCropper.

| Nœud | Réglages conservés |
|---|---|
| `(Down)Load LivePortraitModels` | `precision: fp16` |
| `LivePortrait Load FaceAlignmentCropper` | `face_detector: blazeface` ; `landmarkrunner_device: CPU` ; `face_detector_device: cuda` ; `face_detector_dtype: fp16` ; `keep_model_loaded: true` |
| `Charger Image` | Photo cible de test `photo_test.jpg`, à remplacer par la cible retenue. |
| `Resize Image` | 512 × 512, Lanczos, proportions conservées. |
| `Webcam Capture CV2` | 512 × 512 ; `cam_index: 0` ; `release: false`. |
| `LivePortrait Cropper` | `dsize: 512` ; `scale: 2.34`, valeurs par défaut. |
| `LivePortrait Process` | Valeurs par défaut, notamment `stitching: true` et `relative_motion_mode: single_frame`. |
| `Aperçu Image` | Aperçu agrandi ; une capture dans OBS est envisagée, pas encore réalisée. |

## Emplacements utiles

Le dossier de base de cette installation est `%LOCALAPPDATA%\Comfy-Desktop\ComfyUI-Installs\deepfake\ComfyUI`.

| Élément | Chemin relatif à ce dossier |
|---|---|
| Modèles | `models\liveportrait` |
| Python utilisé pour les dépendances | `.venv\Scripts\python.exe` |
| Fichier corrigé | `custom_nodes\comfyui-liveportraitkj\face_alignment\api.py` |
| Copie de l’original | `custom_nodes\comfyui-liveportraitkj\face_alignment\api_ancien.py` |

## Résultat et limites de l’essai

J’ai obtenu une animation de la photo cible pilotée par la webcam. Aucun relevé d’images par seconde, mesure de latence ou test de stabilité prolongé n’a encore été consigné. La voix, OBS, la synchronisation et le fonctionnement complet hors ligne n’ont pas encore été testés.

[Retour au bilan de la semaine](2026-W46.md) · [Index du journal](README.md)
