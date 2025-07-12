# stt.py

import pyaudio
import websocket
import json
import threading
import time
from urllib.parse import urlencode
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
YOUR_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

CONNECTION_PARAMS = {
    "sample_rate": 16000,
    "format_turns": True,
}
API_ENDPOINT = f"wss://streaming.assemblyai.com/v3/ws?{urlencode(CONNECTION_PARAMS)}"
FRAMES_PER_BUFFER = 800
SAMPLE_RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16

audio = None
stream = None
ws_app = None
audio_thread = None
stop_event = threading.Event()


# speech.py

last_sent = None  # top-level, not inside start_stream or any function

def start_stream(on_transcript_callback):
    global audio, stream, ws_app

    def on_open(ws):
        def stream_audio():
            while not stop_event.is_set():
                try:
                    audio_data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                    ws.send(audio_data, websocket.ABNF.OPCODE_BINARY)
                except Exception as e:
                    print(f"Error streaming audio: {e}")
                    break
        global audio_thread
        audio_thread = threading.Thread(target=stream_audio)
        audio_thread.daemon = True
        audio_thread.start()
        print("🎤 Listening...")

    def on_message(ws, message):
        global last_sent
        try:
            data = json.loads(message)
            if data.get("type") == "Turn":
                # print(json.dumps(data, indent=2))
                if data.get("end_of_turn") and data.get("turn_is_formatted"):
                    transcript = data.get("transcript", "").strip()
                    print(f"🔍 Checking transcript: '{transcript}' | Last sent: '{last_sent}'")
                    if transcript and transcript != last_sent:
                        last_sent = transcript
                        print(f"✅ Sending transcript to callback: {transcript}")
                        on_transcript_callback(transcript)
                    else:
                        print("🛑 Skipped: empty or duplicate transcript")
        except Exception as e:
            print(f"[Error in on_message]: {e}")

    def on_error(ws, error):
        print(f"[WebSocket Error]: {error}")
        stop_event.set()

    def on_close(ws, code, msg):
        print(f"[WebSocket Closed]: {code} - {msg}")
        cleanup()

    def cleanup():
        global stream, audio
        stop_event.set()
        if stream:
            if stream.is_active():
                stream.stop_stream()
            stream.close()
        if audio:
            audio.terminate()
        if audio_thread and audio_thread.is_alive():
            audio_thread.join(timeout=1)

    # Initialize audio stream
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            channels=CHANNELS,
            format=FORMAT,
            rate=SAMPLE_RATE,
        )
    except Exception as e:
        print(f"Failed to open microphone stream: {e}")
        return

    # Setup WebSocket
    ws_app = websocket.WebSocketApp(
        API_ENDPOINT,
        header={"Authorization": YOUR_API_KEY},
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws_thread = threading.Thread(target=ws_app.run_forever)
    ws_thread.daemon = True
    ws_thread.start()

    try:
        while ws_thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("🛑 Keyboard interrupt received.")
        stop_event.set()
        if ws_app.sock and ws_app.sock.connected:
            ws_app.send(json.dumps({"type": "Terminate"}))
        ws_app.close()
        ws_thread.join()
        cleanup()
