import socket
import whisper
import wave
import io

import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Configuration
SERVER_IP = '0.0.0.0'  # Listen on all network interfaces
SERVER_PORT = 12345
CHUNK = 1024
RATE = 16000
CHANNELS = 1
FORMAT = 'int16'

# Initialize Whisper
model = whisper.load_model("base")  # Load a smaller model for better performance

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)
print(f"Server listening on {SERVER_IP}:{SERVER_PORT}...")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

audio_data = b""

try:
    while True:
        data = client_socket.recv(CHUNK)
        if not data:
            break
        audio_data += data

        # Process and transcribe when enough audio data is collected
        if len(audio_data) >= RATE * 2:  # About 1 second of audio
            print("Transcribing audio...")

            # Convert raw audio data to a proper WAV format
            with wave.open("temp_audio.wav", "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)  # 16 bits = 2 bytes
                wf.setframerate(RATE)
                wf.writeframes(audio_data)

            # Transcribe using Whisper
            result = model.transcribe("temp_audio.wav")
            print("Transcription:", result['text'])

            # Clear buffer after processing
            audio_data = b""
except KeyboardInterrupt:
    print("\nServer shutting down...")
finally:
    client_socket.close()
    server_socket.close()
