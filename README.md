# 🛡️ Assist Gatekeeper (Smart Pre-Flight Verifier)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/default)

**Assist Gatekeeper** is a two-stage pre-flight verification integration for Home Assistant Voice Assistant Pipelines.

It acts as an ultra-fast **Intelligent Gatekeeper** placed in front of your heavy Large Language Models (like Gemma 4 12B, Llama 3, Qwen 27B) or primary Conversation Agents.

---

### 💡 Why do you need this?

1. **Eliminates Accidental Triggers & TV Noise**: When your voice satellite or microphone accidentally triggers on background chatter, conversations between people in the room, or dialogue from the television, Gatekeeper inspects the intent in **<100ms** using a compact model like **`gemma2:2b`** on Ollama.
2. **Saves GPU / CPU Cycles**: Your heavy 12B/27B LLM and voice satellite tools (Wikipedia, Web Search, Weather, Entity Cards) are **never executed** on accidental triggers.
3. **Silent Dismissal**: Accidental triggers are silently dismissed—the satellite simply chimes down and goes back to sleep without speaking nonsensical answers or interrupting you.
4. **Transparent Delegation**: When a genuine command is detected (*"enciende la luz"*, *"qué tiempo hace"*), Gatekeeper transparently forwards the entire context and devices to your primary conversation agent (`conversation.ollama_conversation`).

---

### 📦 Installation

#### Method 1: Via HACS (Recommended)
1. Open **HACS** in Home Assistant.
2. Go to **Integrations** → Top right 3 dots → **Custom repositories**.
3. Add `https://github.com/rhythmcreative/assist_gatekeeper` with Category **Integration**.
4. Click **Download**, then restart Home Assistant.

#### Method 2: Manual Installation
Copy `custom_components/assist_gatekeeper` into your Home Assistant `/config/custom_components/` directory and restart.

---

### ⚙️ Configuration

1. In Home Assistant, go to **Settings** → **Devices & Services** → **Add Integration** → Search for **Assist Gatekeeper**.
2. Configure:
   - **Ollama API URL**: (e.g. `http://192.168.68.75:11434`)
   - **Verifier Model**: `gemma2:2b` (runs in ~80ms on Apple Silicon / local GPU).
   - **Target Conversation Agent**: `conversation.ollama_conversation`
   - **Enable Heuristics**: `true` (filters 1-character gibberish, filler sounds like "eh", "ah" instantly).
   - **Silent Discard**: `true`
3. Go to **Settings** → **Voice Assistants** → Select your pipeline (e.g. **Home Assistant**) → Change **Conversation Agent** to **`Assist Gatekeeper`**.
