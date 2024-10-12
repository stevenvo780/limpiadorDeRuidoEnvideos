import ffmpeg
import whisper
import tempfile
import os
import torch

# Archivos de entrada y salida
input_video = "podcast_video.mp4"
output_video = "podcast_video_clean.mp4"

# Verificar si CUDA está disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Usando dispositivo:", device)

# Extraer el audio del video original a un archivo temporal
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
    temp_audio_path = temp_audio.name
    ffmpeg.input(input_video).output(temp_audio_path, acodec="pcm_s16le", ac=1).run()
    print("Audio extraído:", temp_audio_path)

# Cargar el modelo de Whisper en GPU (si disponible)
model = whisper.load_model("base", device=device)  # Cambia "base" por el modelo deseado: "small", "medium", "large"

# Procesar el audio para mejorar la claridad
result = model.transcribe(temp_audio_path, fp16=(device == "cuda"))
enhanced_audio_path = temp_audio_path.replace(".wav", "_enhanced.wav")

# Guardar el audio mejorado
with open(enhanced_audio_path, 'wb') as f:
    f.write(result['audio'])
    print("Audio mejorado guardado en:", enhanced_audio_path)

# Reemplazar el audio del video original con el audio mejorado
ffmpeg.input(input_video).output(output_video, acodec="aac", audio_bitrate="192k").run()
print("Video final guardado en:", output_video)

# Limpiar archivos temporales
os.remove(temp_audio_path)
os.remove(enhanced_audio_path)

print("Proceso completado con éxito.")
