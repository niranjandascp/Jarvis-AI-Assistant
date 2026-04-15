import sounddevice as sd
import wavio

fs = 44100
seconds = 5

print("🎤 Recording for 5 seconds...")

recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()

wavio.write("output.wav", recording, fs, sampwidth=2)

print("✅ Recording saved as output.wav")
