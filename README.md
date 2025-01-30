Audio2Text

📌 Description

Audio2Text est un script Python permettant de transcrire des fichiers audio en texte en utilisant Whisper d'OpenAI. Il détecte automatiquement les silences dans l'audio et segmente l'enregistrement avant de le transcrire pour une meilleure précision.

🚀 Fonctionnalités

🔹 Transcription automatique de fichiers audio en texte

🔹 Détection et segmentation des silences pour améliorer la clarté

🔹 Prise en charge de plusieurs formats audio (MP3, WAV, etc.)

🔹 Génération automatique du fichier de sortie dans le dossier OUTPUTS/

🔹 Gestion améliorée des logs pour un suivi détaillé du processus

🛠️ Installation

1️⃣ Prérequis

Assurez-vous d'avoir Python 3.7+ installé sur votre machine. Ensuite, installez les dépendances nécessaires avec :

pip install -r requirements.txt

Si vous n'avez pas encore installé FFmpeg, ajoutez-le à votre système :

Windows : Téléchargez FFmpeg ici et ajoutez ffmpeg/bin au PATH

Linux (Ubuntu/Debian) :

sudo apt update && sudo apt install ffmpeg

MacOS :

brew install ffmpeg

2️⃣ Installation des modules requis

pip install openai-whisper torch pydub

🎯 Utilisation

Transcrire un fichier audio

Exécutez simplement le script avec :

python Audio2Text.py <nom_du_fichier_audio>

Par exemple :

python Audio2Text.py test.mp3

Le script :

Recherche le fichier dans le dossier INPUTS/ (si aucun chemin absolu n'est fourni)

Détecte les silences et segmente l'audio

Transcrit chaque segment

Enregistre le texte dans OUTPUTS/transcription_YYYYMMDD_HHMMSS.txt

Spécifier un fichier de sortie

python Audio2Text.py test.mp3 mon_fichier_transcrit.txt

Cela enregistrera la transcription dans OUTPUTS/mon_fichier_transcrit.txt

📂 Structure du projet

Audio2Text/
│── INPUTS/                 # Dossier contenant les fichiers audio à transcrire
│── OUTPUTS/                # Dossier où les transcriptions seront enregistrées
│── Audio2Text.py           # Script principal
│── requirements.txt        # Liste des dépendances
│── README.md               # Documentation du projet

⚡ Améliorations futures

🎤 Détection automatique des changements d'orateur

🌍 Prise en charge multilingue

📜 Interface graphique pour simplifier l'utilisation

📝 Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le partager.

💡 Contributions

Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, n'hésitez pas à soumettre une pull request ou à signaler un problème.

🚀 Transformez vos fichiers audio en texte en toute simplicité avec Audio2Text ! 🎙️📜

