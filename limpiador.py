import ffmpeg
import tempfile
import os
import subprocess

# Archivos de entrada y salida
input_video = "podcast_video.mp4"
output_video = "podcast_video_clean.mp4"

# Extraer el audio del video original a un archivo temporal
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
    temp_audio_path = temp_audio.name
    (
        ffmpeg
        .input(input_video)
        .output(temp_audio_path, acodec="pcm_s16le", ac=1)
        .run()
    )
    print("Audio extraído:", temp_audio_path)

# Procesar el audio con Demucs para eliminar el ruido
print("Iniciando reducción de ruido con Demucs...")
subprocess.run(f"demucs --two-stems=vocals {temp_audio_path}", shell=True)

# Ruta del audio limpio generado por Demucs
denoised_audio_path = f"separated/htdemucs/{os.path.basename(temp_audio_path).replace('.wav', '')}/vocals.wav"

# Verificar si el archivo de salida de Demucs existe
if not os.path.exists(denoised_audio_path):
    print("Error: El audio mejorado no se generó.")
    exit(1)

# Reemplazar el audio del video original con el audio mejorado
print("Uniendo audio mejorado al video original...")

# Separar las entradas de video y audio
video_input = ffmpeg.input(input_video)
audio_input = ffmpeg.input(denoised_audio_path)

# Combinar video y audio, especificando los streams
(
    ffmpeg
    .output(
        video_input.video,  # Stream de video original
        audio_input.audio,  # Stream de audio mejorado
        output_video,
        acodec="aac",
        audio_bitrate="192k",
        vcodec="copy"       # Copiar el video sin recodificar
    )
    .run()
)
print("Video final guardado en:", output_video)

# Limpiar archivos temporales
os.remove(temp_audio_path)

print("Proceso completado con éxito.")
