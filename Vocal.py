import sounddevice as sd
import soundfile as sf
import keyboard
import speech_recognition as sr
import paho.mqtt.publish as publish
MQTT_BROKER = "localhost"
MQTT_TOPIC = "home"


def record_audio(filename, duration, samplerate):
    print("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    sf.write(filename, audio_data, samplerate)

def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")
    return None

def send_mqtt_message(message):
    publish.single(MQTT_TOPIC, message, hostname=MQTT_BROKER)

def main():
    while True:
        print("Press 'k' to start recording audio and 'q' to quit.")
        keyboard.wait('k')

        # Record audio for 4 seconds at a sample rate of 44100 Hz
        record_audio("recorded_audio.flac", duration=4, samplerate=44100)

        # Convert audio to text
        try:
            audio_text = audio_to_text("recorded_audio.flac")
            if audio_text:
                print("Recognized text:", audio_text)
                if "hkome" in audio_text:
                    print("Sending to MQTT")
                    send_mqtt_message(audio_text)
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()