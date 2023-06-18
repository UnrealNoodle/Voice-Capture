import pyaudio
import wave
import tempfile
import os

# Set the duration for audio capture in seconds
duration = 5

# Set the file path for saving the audio capture
audio_file = os.path.join(tempfile.gettempdir(), "Audio_Capture.wav")

# Configure the audio recording settings
sample_rate = 44100  # Sample rate in Hz
channels = 2  # Number of audio channels (stereo)
chunk = 1024  # Number of audio frames per buffer

# Create an instance of the PyAudio class
audio = pyaudio.PyAudio()

# Get the default input device index
default_device_index = audio.get_default_input_device_info()["index"]

# Create an input stream using the default device
stream = audio.open(
    format=pyaudio.paInt16,
    channels=channels,
    rate=sample_rate,
    input=True,
    input_device_index=default_device_index,
    frames_per_buffer=chunk
)

print("Recording audio...")

# Start recording
frames = []
for _ in range(int(sample_rate / chunk * duration)):
    data = stream.read(chunk)
    frames.append(data)

print("Recording finished.")

# Stop and close the input stream
stream.stop_stream()
stream.close()

# Terminate the PyAudio instance
audio.terminate()

# Save the recorded audio frames to a WAV file
with wave.open(audio_file, "wb") as wav_file:
    wav_file.setnchannels(channels)
    wav_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(b"".join(frames))

print("Audio saved to:", audio_file)
