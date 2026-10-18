"""Constants for Assist Gatekeeper."""

DOMAIN = "assist_gatekeeper"

CONF_OLLAMA_URL = "ollama_url"
DEFAULT_OLLAMA_URL = "http://192.168.68.75:11434"

CONF_VERIFIER_MODEL = "verifier_model"
DEFAULT_VERIFIER_MODEL = "gemma2:2b"

CONF_TARGET_AGENT = "target_agent"
DEFAULT_TARGET_AGENT = "conversation.ollama_conversation"

CONF_ENABLE_HEURISTICS = "enable_heuristics"
DEFAULT_ENABLE_HEURISTICS = True

CONF_VERIFIER_PROMPT = "verifier_prompt"
DEFAULT_VERIFIER_PROMPT = (
    "Clasifica si la frase es una orden o pregunta dirigida a un asistente inteligente (SI) "
    "o si es ruido, conversación casual entre personas o fragmento de televisión/radio (NO).\n"
    "Responde estrictamente con una sola palabra: \"SI\" o \"NO\"."
)

CONF_SILENT_DISCARD = "silent_discard"
DEFAULT_SILENT_DISCARD = True
