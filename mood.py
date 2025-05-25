

from flask import Flask, render_template, request
import sounddevice as sd
import soundfile as sf
import tempfile
import speech_recognition as sr

app = Flask(__name__)

# Mood response dictionary
responses = {
    "Happy": {
        "quote": "Keep the good vibes going!",
        "activity": "Why not share your joy with a friend?"
    },
    "Sad": {
        "quote": "Tough times don’t last, tough people do.",
        "activity": "Try a 3-minute deep breathing exercise."
    },
    "Stressed": {
        "quote": "You’ve handled worse. Take a deep breath.",
        "activity": "Take a quick walk or stretch your body."
    },
    "Neutral": {
        "quote": "Let’s spark some joy today!",
        "activity": "Write down 3 things you’re grateful for."
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Record 5 seconds of audio
        duration = 5  # seconds
        sample_rate = 44100
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()

        # Save audio to temporary .wav file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            sf.write(f.name, recording, sample_rate)
            audio_file_path = f.name

        # Analyze with speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print("Recognized Text:", text)

        # Mood detection based on keywords
        if any(word in text.lower() for word in ['happy', 'good', 'great', 'awesome']):
            mood = "Happy"
        elif any(word in text.lower() for word in ['sad', 'bad', 'down', 'tired']):
            mood = "Sad"
        elif any(word in text.lower() for word in ['stress', 'stressed', 'pressure']):
            mood = "Stressed"
        else:
            mood = "Neutral"

    except Exception as e:
        print("Error:", e)
        mood = "Neutral"

    return render_template(
        'index.html',
        mood=mood,
        quote=responses[mood]["quote"],
        activity=responses[mood]["activity"]
    )

if __name__ == '_main_':
    app.run(debug=True)


