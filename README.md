<h1 align="center">Assist Gatekeeper</h1>

<div align="center">

<p><i>Ultra-fast two-stage pre-flight intent verification and noise firewall for Home Assistant voice pipelines.</i></p>

[![Home Assistant](https://img.shields.io/badge/Home_Assistant-41BDF5?style=for-the-badge&logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange?style=for-the-badge&logo=hacs&logoColor=white)](https://hacs.xyz/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_AI-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com/)
[![Gemma](https://img.shields.io/badge/Model-Gemma_2:2B-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/gemma)
[![Active](https://img.shields.io/badge/Status-Active-2EA44F?style=for-the-badge)](#)
[![Latency](https://img.shields.io/badge/Latency-<100ms-blueviolet?style=for-the-badge)](#)

<br/>

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=rhythmcreative&repository=assist_gatekeeper&category=integration)

</div>

## About

**Assist Gatekeeper** is an intelligent, high-speed conversation proxy designed for Home Assistant Assist voice pipelines. It acts as an ultra-fast **two-stage pre-flight firewall** in front of your heavy primary Large Language Models (such as `gemma4:12b`, `llama3:70b`, `qwen2.5:32b`) and tool-execution engines.

When voice satellites, smart speakers, or room microphones wake up accidentally from background TV dialogue, casual room chatter, or acoustic artifacts, **Assist Gatekeeper** evaluates the transcribed utterance in under **100 milliseconds** using a lightweight local model (`gemma2:2b` via Ollama). Spurious triggers are discarded silently without waking the heavy GPU model or speaking unwanted error messages, while genuine smart home requests are delegated transparently with zero loss of context.

## Pipeline Comparison

| Scenario | Standard Voice Pipeline | With Assist Gatekeeper |
| :--- | :--- | :--- |
| **TV / Radio Dialogue** | Wakes heavy 12B+ model; triggers tool calls; speaks awkward answers | **Silently discarded in ~130ms**; no speech, zero GPU load |
| **Background Chatter** | Often answers unintended questions or says *"Sorry, I didn't understand"* | **Ignored silently**; satellite quietly returns to sleep |
| **Micro-sounds / Fillers** | Sends single-word noise ("eh", "ah") to the LLM | **Filtered instantly (0ms)** via local regex heuristics |
| **Valid Voice Commands** | Directly invokes heavy LLM (~1.5s - 4s) | **Approved in ~98ms**, transparently passed to primary agent |
| **Tool Execution** | Runs tools on every accidental wake-word false alarm | **Only executes tools** (Weather, Wikipedia, Entities) on real user intent |

## Quick Start

### 1. Installation via HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=rhythmcreative&repository=assist_gatekeeper&category=integration)

1. Click the button above, or manually open **HACS** in your Home Assistant instance.
2. Click the three dots in the top right corner → **Custom repositories**.
3. Add the repository URL:
   ```text
   https://github.com/rhythmcreative/assist_gatekeeper
   ```
4. Set Type to **Integration** and click **Add**.
5. Find **Assist Gatekeeper** in the integration list and click **Download**.
6. Restart Home Assistant Core.

### 2. Manual Installation

Clone or download this repository and copy the `custom_components/assist_gatekeeper` folder into your Home Assistant config directory:

```bash
cd /config/custom_components
git clone https://github.com/rhythmcreative/assist_gatekeeper.git assist_gatekeeper
```

### 3. Pipeline Configuration

1. In Home Assistant, navigate to **Settings** → **Devices & Services** → **Add Integration**.
2. Search for **Assist Gatekeeper** and complete the quick setup wizard.
3. Go to **Settings** → **Voice Assistants** → Select your active pipeline (e.g., **Home Assistant**).
4. Change the **Conversation Agent** to **`Assist Gatekeeper`**.

## How It Works

### 1. Ultra-Fast Pre-Flight Verification
When speech is transcribed by your STT engine, Gatekeeper intercepts the text before it reaches your primary conversation engine. It dispatches a deterministic classification prompt (temperature `0.0`, `num_predict: 3`) to a fast local model (`gemma2:2b`) running on Ollama:
```text
User Speech ──► [STT Engine] ──► [Assist Gatekeeper]
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
      [Noise / TV Dialogue: "NO"]                 [Valid Intent: "SI"]
                   │                                           │
          Silent Discard (<130ms)                Transparent Delegation
        (No speech, zero GPU load)              to Primary LLM (12B+) + Tools
```

### 2. Sub-Millisecond Heuristic Pre-Filter
Before calling the verifier model over the network, Gatekeeper runs an in-memory heuristic pass to weed out empty tokens, single-character acoustic noise, and common vocal fillers (e.g. *"eh"*, *"ah"*, *"mmm"*). These are dismissed in **0 milliseconds**.

### 3. Silent False-Alarm Dismissal
If the utterance is classified as TV audio, radio, or conversation between people in the room, Gatekeeper returns an immediate `action_done` with empty speech. The voice satellite will simply chime down and resume listening without making noise or disrupting the room.

### 4. Transparent Full-Context Delegation
When the intent is verified as genuine (*"enciende la luz"*, *"qué tiempo hace en Madrid"*), Gatekeeper passes the original text, conversation history, and device targeting directly to your primary agent (`conversation.ollama_conversation`). Your tools (Entity Control, Wikipedia, Weather, Web Search) execute normally without delay.

### 5. Multi-Language Ready
Gatekeeper ships with built-in classification prompts for both **Spanish** and **English**, and automatically synchronizes with your voice pipeline's language.

## Configuration Options

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `ollama_url` | String | `http://localhost:11434` | Network endpoint of your Ollama instance hosting the verifier model. |
| `verifier_model` | String | `gemma2:2b` | Fast, compact LLM used for instant intent verification. |
| `target_agent` | String | `conversation.ollama_conversation` | Primary conversation agent to delegate to when intent is valid. |
| `enable_heuristics` | Boolean | `true` | Instant in-memory rejection of micro-phrases and acoustic filler noise. |
| `silent_discard` | Boolean | `true` | Return empty speech on false alarms instead of speaking error messages. |
| `verifier_prompt` | String | *(Built-in)* | System prompt used to instruct the verifier model. |

## Repository Structure

```text
assist_gatekeeper/
├── hacs.json                                    # HACS integration metadata
├── README.md                                    # Project documentation
└── custom_components/
    └── assist_gatekeeper/
        ├── __init__.py                          # Integration lifecycle & setup
        ├── manifest.json                        # Home Assistant integration manifest
        ├── const.py                             # Configuration keys and defaults
        ├── config_flow.py                       # UI configuration & options flow
        ├── conversation.py                      # Two-stage gatekeeper conversation agent
        └── translations/
            ├── en.json                          # English localization
            └── es.json                          # Spanish localization
```

## Requirements

* **Home Assistant:** 2024.1.0 or newer (Supervised, OS, or Container).
* **Ollama Server:** Local instance running on Apple Silicon, Linux GPU, or network host.
* **Verifier Model:** `gemma2:2b` (recommended), `qwen2.5:1.5b`, or any lightweight instruction model.

```bash
# Pull the recommended verifier model on your Ollama server
ollama pull gemma2:2b
```

## Disclaimer

This is an unofficial community integration and is not affiliated with or endorsed by Nabu Casa or Google.

<div align="center">

<p>Made with ❤️ from rhythmcreative.</p>

</div>
