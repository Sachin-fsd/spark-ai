# import speech_recognition as sr
# # import whisper
# import pyttsx3


# recognizer = sr.Recognizer()
# # Load models once
# # whisper_model = whisper.load_model("base")  # or "small" for faster
# samplerate = 44100  # Define the samplerate

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def listen_for_hotword(hotwords=["sun", "hello", "bhai", "brother", "alex", "dear", "listen"]):
#     with sr.Microphone() as source:
#         print("👂 Listening for hotwords...")
#         audio = recognizer.listen(source, phrase_time_limit=4)
#         try:
#             text = recognizer.recognize_google(audio).lower()
#             print("🎧 You said:", text)
#             # Check if any hotword is in the recognized text
#             return any(hotword in text for hotword in hotwords)
#         except Exception as e:
#             print("⚠️ Error:", str(e))
#             return False
        
# def transcribe_with_google_sr():
#     speak("What is the command sir?")
#     print("🎤 Speak your command...")
#     try:
#         with sr.Microphone() as source:
#             audio = recognizer.listen(source, phrase_time_limit=6)
#             text = recognizer.recognize_google(audio).strip()
#             return text
#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#         return "nothing do nothing"
#     except sr.RequestError as e:
#         print(f"Could not request results from Google Speech Recognition service; {e}")
#         return "nothing do nothing"
#     except Exception as e:
#         print(f"An unexpected error occurred during transcription: {e}")
#         return "nothing do nothing"

import whisper
import pyttsx3
import sounddevice as sd
import numpy as np

# Load the Whisper model once
try:
    whisper_model = whisper.load_model("base")  # or "small" for faster
except Exception as e:
    print(f"⚠️ Error loading Whisper model: {e}")
    whisper_model = None

samplerate = 16000  # Standard sample rate for Whisper
channels = 1       # Mono audio

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def record_audio(duration=4):
    """Records audio for a specified duration using sounddevice."""
    print("👂 Recording...")
    try:
        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype='int16')
        sd.wait()  # Wait until recording is finished
        return audio_data.flatten().astype(np.float32) / 32768.0
    except Exception as e:
        print(f"⚠️ Error during recording: {e}")
        return None

def transcribe_audio(audio_data):
    """Transcribes the given audio data using the Whisper model."""
    if whisper_model and audio_data is not None:
        try:
            result = whisper_model.transcribe(audio_data, fp16=False)
            return result["text"].lower().strip()
        except Exception as e:
            print(f"⚠️ Error during transcription: {e}")
            return None
    else:
        print("⚠️ Whisper model not loaded or no audio data.")
        return None

def listen_for_hotword(hotwords=["sun", "hello", "bhai", "brother", "alex", "dear", "listen"]):
    """Listens for a hotword using Whisper."""
    print("👂 Listening for hotwords...")
    audio_data = record_audio(duration=4)
    if audio_data is not None:
        text = transcribe_audio(audio_data)
        if text:
            print("🎧 You said:", text)
            return any(hotword in text for hotword in hotwords)
    return False

def transcribe():
    """Records audio and transcribes it as a command using Whisper."""
    speak("What is the command sir?")
    print("🎤 Speak your command...")
    audio_data = record_audio(duration=6)
    if audio_data is not None:
        command = transcribe_audio(audio_data)
        return command if command else "nothing do nothing"
    else:
        return "nothing do nothing"
