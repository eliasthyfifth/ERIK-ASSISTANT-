# ERIK v3 🤖

ERIK is a lightweight, local-first AI system watchdog and desktop assistant for Linux. 

She runs quietly in the background, monitors your system resources (CPU, RAM, Battery), reacts to power events (Sleep/Wake), and features a sassy, energetic personality powered by a tiny local LLM (`qwen3:0.6b`) and Kokoro-ONNX TTS.

## Features
* **Local Brain:** Uses Ollama and `qwen3:0.6b` for conversational replies without needing the internet.
* **Context Aware:** Injects real-time system stats (RAM/CPU/Battery) into her context so she always knows how your PC is doing.
* **Voice Feedback:** High-quality local Text-to-Speech using Kokoro-ONNX (Configured with a custom Kasane Teto voice blend).
* **Systemd Integration:** Runs as a background user service.
* **GTK Pop-up Client:** Hit a shortcut to chat with her instantly.

## 🛠️ Project Structure

```text
ERIK/
├── src/                    # Core daemon logic
│   ├── main.py             # Entry point
│   ├── brain.py            # Ollama LLM integration
│   ├── tts.py              # Kokoro-ONNX audio engine
│   ├── watchdog.py         # Resource monitoring (psutil)
│   ├── event_listener.py   # DBus sleep/wake triggers
│   ├── bridge.py           # Socket server for the client
│   └── utils.py            # Desktop notifications
├── models/                 # AI Models (NOT committed to git)
│   ├── kokoro-v1.0.onnx    # ~300MB TTS Model
│   ├── voices-v1.0.bin     # ~27MB Voice Embeddings
│   └── teto_voice.npy      # Custom voice blend
├── cloning/                # Scripts used for voice tuning
├── erik_client.py          # The GTK UI for chatting
├── erik-watchdog.service   # Systemd service file
├── config.yaml             # Settings and message customization
└── requirements.txt        # Python dependencies
```

## 🚀 Setup & Installation

### 1. Prerequisites
You need **Python 3**, **Ollama**, and **systemd** (Linux).

```bash
# Install Ollama and pull the tiny brain
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:0.6b
```

### 2. Clone and Setup Environment
```bash
git clone https://github.com/YOUR_USERNAME/ERIK.git
cd ERIK
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Download the TTS Models
The Kokoro models are too large for GitHub. You must download them manually into the `models/` directory:
1. Download `kokoro-v1.0.onnx` and `voices-v1.0.bin` from [HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M/tree/main).
2. Place them in the `ERIK/models/` folder.

### 4. Enable the Background Service
```bash
mkdir -p ~/.config/systemd/user/
ln -sf $(pwd)/erik-watchdog.service ~/.config/systemd/user/erik-watchdog.service
systemctl --user daemon-reload
systemctl --user enable --now erik-watchdog.service
```

## 💬 How to Chat
Run the client script to bring up the GTK chat window. It is recommended to bind this to a global keyboard shortcut (e.g., `Ctrl+Alt+E`).
```bash
/path/to/ERIK/venv/bin/python /path/to/ERIK/erik_client.py
```