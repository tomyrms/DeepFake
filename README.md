# DeepFake, projet scolaire

Nous sommes Tomas et Robin. Nous préparons une démonstration par webcam qui transforme la tête d’une personne, cheveux compris. Les participants seront consentants et le public saura que les images sont générées par IA.

La présentation est envisagée pour les portes ouvertes du 15 janvier 2027. La date reste à confirmer avec l’école.

## Où nous en sommes

Nous avons retenu JoyAI-Video-Edit après un essai de sa démo sur Hugging Face. Nous voulons maintenant l’installer sur une RTX 5090 de 32 Go de VRAM louée chez SwissGPU. Le [rapport sur les choix techniques](docs/documentation-technique/rapport-choix-techniques.md) explique les besoins du modèle, les autres solutions étudiées et le coût du test.

Les premiers essais nous ont permis de préciser ce que nous cherchons :

- Deep-Live-Cam était trop lent et saccadé sur notre PC. Il remplaçait le visage, sans transformer les cheveux ni le reste de la tête.
- Nous avons essayé FasterLivePortrait les 11 et 12 novembre, en vidéo, dans son interface web et avec la webcam. La vidéo d’exemple tournait autour de 14 images/s, mais le résultat ne correspondait pas à notre objectif.
- Le 12 novembre, Robin a animé une photo avec la webcam dans ComfyUI-LivePortraitKJ. La voix et OBS restent à tester.

L’essai de JoyAI sur le serveur doit encore confirmer le rendu, la fluidité et le délai depuis l’école.

## Suivre le projet

- [Journal de travail](docs/journal/README.md)
- [Documentation technique](docs/documentation-technique/README.md)
- [Planning et tableau de suivi](https://github.com/users/tomyrms/projects/3)
- [Issues](https://github.com/tomyrms/DeepFake/issues)
- [Organisation du travail](docs/organisation.md)

Le journal contient une page par semaine. Les issues suivent le travail terminé et les prochaines tâches choisies. Le Gantt garde les réalisations, avec leurs dates connues.
