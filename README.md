# DeepFake — projet scolaire

Nous sommes **Tomas et Robin**. Nous préparons une démonstration de transformation générative de la tête, cheveux compris, en direct par webcam. Après un premier essai de Deep-Live-Cam sur notre PC, nous avons choisi de tester une RTX 5090 louée chez SwissGPU pour disposer de davantage de ressources. L’objectif est de montrer le fonctionnement de cette technologie, ses possibilités et ses limites à partir de participants consentants. Le caractère synthétique des images sera annoncé clairement.

La présentation est envisagée pour les portes ouvertes du **15 janvier 2027, date à confirmer avec l’école**.

## Où en sommes-nous ?

Au 13 novembre 2026, nous avons organisé le projet, étudié le matériel et réalisé plusieurs essais vidéo. OpenProject a d’abord été mis en place ; nous avons ensuite choisi GitHub pour réunir le suivi du travail, la documentation et le futur code.

**Nous avons testé Deep-Live-Cam sur notre PC : le traitement était trop lent, saccadé et de qualité insuffisante pour le temps réel.** L’échange concernait uniquement le visage, sans remplacer les cheveux ni le reste de la tête. Ces observations ne sont pas encore accompagnées de mesures de débit ou de délai. Le logiciel utilise bien de l’IA, mais son résultat ne répond pas à notre objectif de transformation complète de la tête ; une solution adaptée reste à sélectionner.

Le **12 novembre**, Robin a obtenu une **animation de photo pilotée par la webcam avec Comfy Desktop et ComfyUI-LivePortraitKJ**. Cette étape vidéo fonctionne ; la voix, OBS, la synchronisation et la répétition complète hors ligne restent non réalisés. Le [bilan de la semaine du 9 au 15 novembre](docs/journal/2026-W46.md) rassemble les contributions de Tomas et Robin, avec les [réglages et corrections techniques](docs/journal/2026-W46-notes-techniques.md).

**Nous avons choisi de tester une RTX 5090 de 32 Go de VRAM chez SwissGPU**, à **0,55 CHF/h hors électricité et frais**. Le [rapport illustré sur les choix techniques](docs/rapport-choix-techniques.md) présente les cartes et fournisseurs avec des images sourcées, explique les alternatives et précise le budget proposé. Les essais permettront de confirmer l’utilisation de cette solution pour la démonstration finale.

## Suivre le projet

- [Planning et tableau de suivi](https://github.com/users/tomyrms/projects/3)
- [Issues terminées](https://github.com/tomyrms/DeepFake/issues?q=is%3Aissue%20is%3Aclosed)
- [Rapports hebdomadaires](docs/journal/README.md)
- [Comment on travaille à deux](docs/organisation.md)
- [Semaine 46 — du 9 au 15 novembre 2026](docs/journal/2026-W46.md)
- [Recherche sur les outils et le matériel](docs/recherche-materiel.md)
- [Rapport illustré — choix techniques et location GPU](docs/rapport-choix-techniques.md)
Les issues et le Gantt conservent désormais les travaux terminés. Nous compléterons le suivi au fur et à mesure des réalisations, sans planifier toutes les tâches à l’avance. Les comptes rendus sont regroupés **par semaine**, avec les dates réelles des contributions. L’[export PDF du 10 novembre](docs/exports/synthese-et-gantt.pdf) reste une archive de l’ancien planning.

Nous privilégions les outils ouverts et une installation reproductible. La licence du logiciel et celles de ses modèles seront examinées séparément avant de retenir une solution.

## Prochain travail

Sélectionner un modèle capable de transformer la tête et les cheveux, puis le tester sur la RTX 5090 en mesurant la qualité, la fluidité et le délai. Vérifier l’accélération GPU et les réglages, confirmer le coût de l’électricité et le financement de la séance, puis valider le trajet vidéo depuis le réseau de l’école. Les professeurs pourront recevoir le journal, le bilan et le planning en PDF.
