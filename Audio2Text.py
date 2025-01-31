import whisper
import os
import sys
import logging
import time
from pydub import AudioSegment, silence
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Définition des dossiers d'entrée et de sortie
INPUT_DIR = "INPUTS/"
OUTPUT_DIR = "OUTPUTS/"

# Création du dossier de sortie s'il n'existe pas
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_file_names():
    """ Récupère les noms de fichiers depuis les arguments de la ligne de commande. """
    if len(sys.argv) < 2:
        logging.error("Usage: python script.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        input_file = os.path.join(INPUT_DIR, input_file)
        if not os.path.exists(input_file):
            logging.error(f"Le fichier '{input_file}' n'existe pas.")
            sys.exit(1)
    
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    output_file = os.path.join(OUTPUT_DIR, output_file)
    
    return input_file, output_file

def detect_silences(audio, silence_thresh=-40, min_silence_len=700):
    """ Détecte les silences dans un fichier audio. """
    logging.info("Analyse de l'audio pour détecter les silences...")
    silence_chunks = silence.detect_silence(audio, min_silence_len, silence_thresh)
    logging.info(f"{len(silence_chunks)} silences détectés.")
    return [(start / 1000, end / 1000) for start, end in silence_chunks]  # Convertir en secondes

def split_audio_on_silence(audio, silence_chunks, enable_segmentation=True):
    """ Découpe l'audio en segments en fonction des silences détectés. """
    if not enable_segmentation:
        logging.info("Segmentation désactivée, utilisation de l'audio entier.")
        return [(0, len(audio) / 1000)]
    
    logging.info("Découpage de l'audio en segments...")
    segments = []
    prev_end = 0
    for start, end in silence_chunks:
        if start - prev_end > 1:  # Éviter les segments trop courts
            segments.append((prev_end, start))
        prev_end = end
    if prev_end < len(audio) / 1000:
        segments.append((prev_end, len(audio) / 1000))
    logging.info(f"{len(segments)} segments d'audio générés.")
    return segments

def transcribe_audio(segments, audio, model):
    """ Transcrit les segments audio détectés à l'aide du modèle Whisper. """
    transcription = []
    for i, (start, end) in enumerate(segments):
        logging.info(f"Transcription du segment {i+1}/{len(segments)} (de {start:.2f}s à {end:.2f}s)...")
        segment_audio = audio[start * 1000:end * 1000]
        segment_path = f"segment_{i}.wav"
        segment_audio.export(segment_path, format="wav")
        
        # Transcription du segment avec langue forcée en français
        result = model.transcribe(segment_path, language="fr")
        transcription.append(f"[Orateur {i+1}] {result['text']}\n")
        
        # Nettoyage du fichier temporaire
        os.remove(segment_path)
    logging.info("Transcription terminée pour tous les segments.")
    return transcription

def main():
    """ Fonction principale du script. """
    start_time = time.time()
    
    # Récupération des noms de fichiers
    input_file, output_file = get_file_names()
    
    logging.info(f"Fichier d'entrée : {input_file}")
    logging.info(f"Fichier de sortie : {output_file}")
    
    # Charger le modèle Whisper
    logging.info("Chargement du modèle Whisper... Cela peut prendre un moment...")
    model = whisper.load_model("medium")
    logging.info("Modèle Whisper chargé avec succès !")
    
    # Chargement et conversion de l'audio
    logging.info("Chargement du fichier audio...")
    audio = AudioSegment.from_file(input_file)
    
    # Détection des silences
    silence_chunks = detect_silences(audio)
    
    # Découpage de l'audio (peut être désactivé)
    enable_segmentation = False  # Désactiver le découpage en segments
    segments = split_audio_on_silence(audio, silence_chunks, enable_segmentation)
    
    # Transcription
    transcription = transcribe_audio(segments, audio, model)
    
    # Écriture de la transcription dans un fichier
    logging.info("Sauvegarde de la transcription...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(transcription)
    
    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f"Transcription terminée en {total_time:.2f} secondes ! Fichier enregistré sous {output_file}")
    print(f"✅ Transcription terminée en {total_time:.2f} secondes ! Fichier enregistré sous {output_file}")

if __name__ == "__main__":
    main()
