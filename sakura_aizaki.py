import openai
import pyaudio
import wave
import tempfile
import requests
from deep_translator import DeepL
from io import BytesIO
import simpleaudio as sa

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"

# Set your DeepL API key here
deepl_api_key = "YOUR_DEEPL_API_KEY"

class SakuraAizaki:
    def __init__(self, speaker_id=1, speed=1.0, pitch=0.0, intonation=1.0, volume=0.0):
        self.translator = Translator()
        self.voicevox_api_url = "http://127.0.0.1:50021"
        self.speaker_id = speaker_id
        self.speed = speed
        self.pitch = pitch
        self.intonation = intonation
        self.volume = volume

    def set_speaker_id(self, speaker_id):
        self.speaker_id = speaker_id

    def set_speed(self, speed):
        self.speed = speed

    def set_pitch(self, pitch):
        self.pitch = pitch

    def set_intonation(self, intonation):
        self.intonation = intonation

    def set_volume(self, volume):
        self.volume = volume

    def record_voice(self, seconds=5):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 1024

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        print("Sakura: Please speak. Recording for", seconds, "seconds...")
        frames = []
        for _ in range(0, int(RATE / CHUNK * seconds)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with tempfile.NamedTemporaryFile(delete=True) as f:
            wave_file = wave.open(f.name, 'wb')
            wave_file.setnchannels(CHANNELS)
            wave_file.setsampwidth(audio.get_sample_size(FORMAT))
            wave_file.setframerate(RATE)
            wave_file.writeframes(b''.join(frames))
            wave_file.close()
            f.seek(0)
            return f.read()

    def transcribe(self, audio_data):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Transcribe the following English audio to text: {audio_data}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        return response.choices[0].text.strip()

    def chatbot_response(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Sakura Aizaki: {prompt}",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        return response.choices[0].text.strip()

    def translate(self, text, dest_language='ja'):
        translator = DeepL(api_key=deepl_api_key)
        translated_text = translator.translate(text, target_lang=dest_language)
        return translated_text

    def text_to_speech(self, text):
        response = requests.post(
            f"{self.voicevox_api_url}/audio_query",
            json={
                "text": text,
                "speaker": self.speaker_id,
                "speed": self.speed,
                "pitch": self.pitch,
                "intonation": self.intonation,
                "volume": self.volume
            }
        )
        audio_query = response.json()
        response = requests.post(
            f"{self.voicevox_api_url}/synthesis",
            json=audio_query
        )
        audio_data = response.content
        return audio_data

    def play_audio(self, audio_data):
        wave_obj = sa.WaveObject.from_wave_file(BytesIO(audio_data))
        play_obj = wave_obj.play()
        play_obj.wait_done()

    def chat(self):
        print("Sakura Aizaki: こんにちは！私はあなたの言葉を日本語に翻訳できます。")
        while True:
            audio_data = self.record_voice()
            transcribed_text = self.transcribe(audio_data)
            print(f"You: {transcribed_text}")
            if transcribed_text.lower() == "quit":
                break
            chatbot_response = self.chatbot_response(transcribed_text)
            translated_response = self.translate_to_japanese(chatbot_response)
            print(f"Sakura Aizaki (Japanese text): {translated_response}")
            audio_response = self.text_to_speech(translated_response)
            self.play_audio(audio_response)