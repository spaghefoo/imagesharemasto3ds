# Projet imageuploader for 3ds and wiiu

Projet de site visant a réimplémenter la fonctionnalité de partage d'image de 3ds et de wiiu du [Site Officiel Nintendo](https://i.nintendo.net)

## Features
    - Partage d'images 3ds et wiiu(sur mastodon pour l'instant uniquement) avec style adapté a ces consoles.
    - Detection de l'user agent
    - Traduction primitive en français et en anglais.

## Fonctionnalités prevues(un jour)
    - Publication d'images sur bluesky(et facebook)
    - Ajout d'un a propos si on se connecte sur un ordinateur



Pour lancer le projet Activer l'environnement virtuel(.\Scripts\activate)
Télécharger les dependances (pip -r requirement.txt)

Puis lancer: flask --app web3DsBackend run --debug --host 0.0.0.0