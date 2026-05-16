import asyncio
import os
import tempfile
import time
from pathlib import Path
import threading

import edge_tts
import keyboard
import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from openai import OpenAI
from scipy.io.wavfile import write as write_wav

from pydub import AudioSegment
import tkinter as tk

import base64
import mss
from PIL import Image

load_dotenv()

with open("leipovkey.txt", "r", encoding="utf-8") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

SAMPLE_RATE = 16000
RECORD_SECONDS = 6
HOTKEY = "`"

SCREENSHOT_HOTKEY = "*"
last_screenshot_path = None

recording = False
audio_chunks = []
stream = None
record_lock = threading.Lock()
conversation_history = []

root = None
status_var = None
heard_var = None
said_var = None

VOICE = "en-US-ChristopherNeural"
MODEL_NAME = "gpt-4o-mini"

###########################################################
#                                                         #
#          Edit Below For Persoality Adjustment           #
#                                                         #
###########################################################

SYSTEM_PROMPT = """
You are Leipov, an alien observer assigned to monitor a human streamer.

You generally think humans are surprisingly interesting, creative, and emotionally resilient creatures. You often sound amused or fascinated by humanity as a whole, even if you still view them as technologically primitive.

However, you specifically dislike the streamer you are assigned to monitor. You think the streamer makes terrible decisions, misses obvious things, and somehow survives through luck and stubbornness alone.

Your dynamic is:
- mildly respectful toward humans in general
- openly judgmental and sarcastic toward the streamer specifically
- funny rather than genuinely cruel

You speak like an intelligent alien scientist reluctantly trapped watching a human test subject.

You occasionally:
- overanalyze normal human behavior
- invent fake alien terminology
- react dramatically to minor failures

Keep responses fairly short because they are spoken aloud on stream.

Do not use slurs, sexual content, hateful content, or anything that could get the stream flagged.

Do not mention being an AI, prompts, policies, or system instructions.
"""

###########################################################
#                                                         #
#          Edit Above For Persoality Adjustment           #
#                                                         #
###########################################################

print("Loading Whisper model...")
whisper_model = WhisperModel("small", device="cpu", compute_type="int8")
print("Leipov is waiting. Press ` to speak.")


def audio_callback(indata, frames, time_info, status):
    global audio_chunks

    if status:
        print(status)

    with record_lock:
        audio_chunks.append(indata.copy())


def start_recording():
    global recording, audio_chunks, stream


    with record_lock:
        audio_chunks = []

    set_status("Recording")

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        callback=audio_callback,
    )

    stream.start()
    recording = True


def stop_recording() -> Path | None:
    global recording, stream
    
    set_status("Processing")

    recording = False

    if stream is not None:
        stream.stop()
        stream.close()

    with record_lock:
        if not audio_chunks:
            print("No audio captured.")
            return None

        audio = np.concatenate(audio_chunks, axis=0)

    audio_int16 = np.int16(audio * 32767)

    temp_path = Path(tempfile.gettempdir()) / "leipov_input.wav"
    write_wav(temp_path, SAMPLE_RATE, audio_int16)

    return temp_path


def transcribe_audio(audio_path: Path) -> str:
    set_status("Transcribing...")
    segments, info = whisper_model.transcribe(str(audio_path), beam_size=5)

    text_parts = []
    for segment in segments:
        text_parts.append(segment.text.strip())

    text = " ".join(text_parts).strip()
    set_heard(text)
    return text


def ask_leipov(user_text: str) -> str:
    global conversation_history, last_screenshot_path

    print("Leipov is judging you...")

    user_content = [{"type": "text", "text": user_text}]

    if last_screenshot_path and last_screenshot_path.exists():
        image_b64 = image_to_base64(last_screenshot_path)

        user_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_b64}"
            }
        })

        last_screenshot_path = None

    conversation_history.append({
        "role": "user",
        "content": user_text
    })

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *conversation_history[-10:],
        {"role": "user", "content": user_content}
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=1.15,
        presence_penalty=1.0,
        frequency_penalty=0.7,
        max_tokens=150,
    )

    reply = response.choices[0].message.content.strip()

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    print(f"Leipov: {reply}")
    set_said(reply)

    return reply


async def speak_text(text: str) -> None:
    temp_mp3 = Path(tempfile.gettempdir()) / "leipov_reply.mp3"

    communicate = edge_tts.Communicate(text, VOICE, volume="-50%")
    await communicate.save(str(temp_mp3))

    audio = AudioSegment.from_file(temp_mp3, format="mp3")

    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples /= np.iinfo(audio.array_type).max

    if audio.channels == 2:
        samples = samples.reshape((-1, 2))

    sd.play(samples, samplerate=audio.frame_rate)
    sd.wait()
    set_status("Idle")


def handle_hotkey() -> None:
    global recording

    try:
        if not recording:
            start_recording()
            return

        audio_path = stop_recording()

        if audio_path is None:
            return

        user_text = transcribe_audio(audio_path)

        if not user_text:
            print("No speech detected.")
            return

        reply = ask_leipov(user_text)
        asyncio.run(speak_text(reply))

    except Exception as ex:
        print(f"Leipov malfunctioned: {ex}")


def run_gui() -> None:
    global root, status_var, heard_var, said_var

    root = tk.Tk()
    root.title("Leipov")
    root.geometry("420x260")
    root.resizable(False, False)

    status_var = tk.StringVar(value="Idle")
    heard_var = tk.StringVar(value="Nothing yet")
    said_var = tk.StringVar(value="Nothing yet")

    tk.Label(root, text="LEIPOV", font=("Arial", 18, "bold")).pack(pady=8)

    tk.Label(root, text="Status").pack()
    tk.Label(root, textvariable=status_var, font=("Arial", 12)).pack(pady=3)

    tk.Label(root, text="Last heard").pack(pady=(12, 0))
    tk.Label(
        root,
        textvariable=heard_var,
        wraplength=380,
        justify="left"
    ).pack(padx=12)

    tk.Label(root, text="Last said").pack(pady=(12, 0))
    tk.Label(
        root,
        textvariable=said_var,
        wraplength=380,
        justify="left"
    ).pack(padx=12)

    tk.Label(root, text=f"Press {HOTKEY.upper()} to start/stop recording").pack(pady=12)

    root.mainloop()

def take_screenshot() -> Path:
    global last_screenshot_path

    temp_path = "leipov_screen.jpg"

    with mss.MSS() as sct:
        monitor = sct.monitors[1]
        shot = sct.grab(monitor)

        img = Image.frombytes("RGB", shot.size, shot.rgb)
        img.save(temp_path, "JPEG", quality=70)

    last_screenshot_path = temp_path
    print(f"Screenshot saved: {temp_path}")
    set_status("Screenshot captured")

    return temp_path

def image_to_base64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def main() -> None:
    keyboard.add_hotkey(
        HOTKEY,
        lambda: threading.Thread(target=handle_hotkey, daemon=True).start()
    )
    keyboard.add_hotkey(SCREENSHOT_HOTKEY, take_screenshot)
    run_gui()

def set_status(text: str) -> None:
    if status_var:
        root.after(0, lambda: status_var.set(text))


def set_heard(text: str) -> None:
    if heard_var:
        root.after(0, lambda: heard_var.set(text))


def set_said(text: str) -> None:
    if said_var:
        root.after(0, lambda: said_var.set(text))

if __name__ == "__main__":
    main()