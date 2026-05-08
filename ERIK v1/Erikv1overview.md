# ERIK v1 - Project Overview & Capabilities

Welcome to the first stable release of **ERIK**. This document outlines exactly what she is capable of and how she interacts with your Linux system.

## 🎭 The Personality: Kasane Teto (Blend E)
ERIK isn't just a script; she has a soul (well, a digital one).
*   **Voice:** Powered by the Kokoro-82M engine using a custom-blended Kasane Teto profile (**Blend E**).
*   **Tone:** Sassy, energetic, and slightly unpredictable. She uses Japanese-isms (desu, baka) and isn't afraid to tell you how she feels about your system usage.

## 🛡️ System Watchdog (Monitoring)
ERIK keeps a constant eye on your hardware resources so you don't have to.
*   **Battery Monitoring:** Warns you when the battery is low and reminds you to find a charger.
*   **RAM Alerts:** detects memory spikes and tells you to close some applications before the system lags.
*   **CPU Tracking:** Monitors sustained high CPU load and complains about "feeling hot."
*   **Cooldown Logic:** She has built-in cooldowns (default 3 minutes) so she doesn't nag you too often.

## ⚡ Power Event Reactivity
ERIK is deeply integrated with your system's power states via DBus.
*   **Startup:** Welcomes you as soon as you log in.
*   **Shutdown:** Says a final goodbye before the system powers off.
*   **Suspend (Sleep):** Bids you goodnight when you close your laptop or trigger sleep.
*   **Resume (Wake):** Features the iconic *"Fuck you, I was sleeping!"* greeting when the system wakes up.

## 🧠 Local Brain (Conversational AI)
You can have a two-way conversation with ERIK, and the best part is it's **100% offline**.
*   **Ollama Integration:** Uses the `qwen3:0.6b` model for ultra-fast, local replies.
*   **Context Awareness:** ERIK doesn't guess your stats. When you ask "How much RAM am I using?", she secretly checks your actual system data before answering.
*   **Memory:** Remembers the last 10 exchanges in your conversation to maintain context.

## 🖥️ Desktop Interaction
*   **GTK Chat Interface:** A native GNOME-style pop-up window (triggered by a keyboard shortcut) for typing messages.
*   **Visual Notifications:** Every time ERIK speaks, a desktop notification appears, ensuring you never miss an alert even if your volume is down.

## ⚙️ Full Customization
Everything is editable via the `config.yaml` file:
*   Change her voice speed.
*   Rewrite every single one of her "brainrot" lines.
*   Adjust the thresholds for RAM, CPU, and Battery warnings.

---
*Developed with love for Arch Linux and Teto fans everywhere.*
