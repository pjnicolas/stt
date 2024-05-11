import sounddevice as sd
import numpy as np
from pynput import keyboard
import scipy.io.wavfile as wav
import time
import openai
import threading
import pydub
from plyer import notification

openai.api_key = "sk-xxx"

sample_rate = 44100
channels = 2
file_number = 1

is_recording = False
stream = None

audio_data = []
last_ctrl_press_time = 0
ctrl_press_interval = 0.2  # 200 milliseconds
max_recording_length = 15 * 60 * sample_rate  # 15 minutes in samples

def callback(indata, frames, time, status):
    """This function is called for each audio frame."""
    global audio_data, is_recording, stream
    audio_data.append(indata.copy())
    if len(audio_data) * len(indata) >= max_recording_length:
        print(" >>> Stop recording due to max length <<<")
        notification.notify(
            title = "Speech To Text",
            message = "Stop recording due to max length",
            timeout = 1
        )
        is_recording = False
        stream.stop()
        stream.close()
        audio_data = []

def transcribe_audio(file_number):
    """Transcribe audio using OpenAI's Whisper model."""
    with open(f"{file_number}.mp3", "rb") as audio_file:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="es"
        )
    cleaned_text = response.text.replace("Subtítulos realizados por la comunidad de Amara.org", "")
    print("[Transcription]", cleaned_text)
    keyboard_controller = keyboard.Controller()
    keyboard_controller.type(cleaned_text + " ")

def transcribe_in_thread(file_path):
    """Function to handle transcription in a separate thread."""
    thread = threading.Thread(target=transcribe_audio, args=(file_path,))
    thread.start()

def convert_and_save(file_number, recording):
    """Converts the WAV recording to MP3 and saves it."""
    filename_wav = f"{file_number}.wav"
    filename_mp3 = f"{file_number}.mp3"
    wav.write(filename_wav, sample_rate, recording)
    sound = pydub.AudioSegment.from_wav(filename_wav)
    sound.export(filename_mp3, format="mp3")

def on_press(key):
    global is_recording, audio_data, stream, last_ctrl_press_time, file_number

    try:
        if key == keyboard.Key.alt_l:
            if is_recording:
                stream.stop()
                stream.close()
                recording = np.concatenate(audio_data, axis=0)
                convert_and_save(file_number, recording)
                transcribe_in_thread(file_number)
                audio_data = []
                stream = sd.InputStream(callback=callback, channels=channels, samplerate=sample_rate)
                stream.start()
                file_number += 1

        if key == keyboard.Key.ctrl_l:
            current_time = time.time()

            if (current_time - last_ctrl_press_time) <= ctrl_press_interval:
                if is_recording:
                    print("[Stop recording]")
                    notification.notify(
                        title = "Speech To Text",
                        message = "Stop recording ",
                        timeout = 1
                    )
                    is_recording = False
                    stream.stop()
                    stream.close()
                    recording = np.concatenate(audio_data, axis=0)
                    convert_and_save(file_number, recording)
                    transcribe_in_thread(file_number)
                    audio_data = []
                else:
                    print("[Start recording]")
                    notification.notify(
                        title = "Speech To Text",
                        message = "Iniciando grabación",
                        timeout = 1
                    )
                    is_recording = True
                    file_number = 1
                    stream = sd.InputStream(callback=callback, channels=channels, samplerate=sample_rate)
                    stream.start()

            last_ctrl_press_time = current_time
    except AttributeError:
        pass

def start_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

if __name__ == '__main__':
    print("Double press 'Ctrl' quickly to start or stop and save the recording.")
    start_listener()
