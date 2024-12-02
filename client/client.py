import socket
import pyaudio

# Configuration
SERVER_IP = '192.168.1.238'
SERVER_PORT = 12345
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, frames_per_buffer=CHUNK)

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Streaming audio...")
    
    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            client_socket.sendall(data)
        except Exception as e:
            print(f"Error while streaming: {e}")
            break
except Exception as e:
    print(f"Could not connect to server: {e}")
finally:
    print("\nStopping audio streaming...")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    client_socket.close()
