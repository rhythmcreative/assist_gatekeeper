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
    "Eres un clasificador binario estricto para un asistente de voz inteligente en el hogar.\n"
    "Determina si la frase transcrita está dirigida al asistente (SI) o si es una activación accidental (NO).\n\n"
    "CRITERIOS PARA \"SI\" (APROBAR - PETICIÓN REAL AL ASISTENTE):\n"
    "- Control domótico y del hogar: encender, apagar, regular luces, persianas, clima, aire, calefacción, enchufes, cerraduras, aspiradora.\n"
    "- Preguntas de tiempo o clima: pronóstico, temperatura, lluvia, viento en cualquier ciudad o ubicación.\n"
    "- Preguntas de hora, fecha o calendario: qué hora es, qué día es hoy, qué tengo en la agenda.\n"
    "- Consultas de información o conocimiento general: qué, quién, cuándo, dónde, cómo o por qué ocurrió algo, biografías, historia, ciencia, países, definiciones, recetas.\n"
    "- Control de música y sonido: reproducir canciones, artistas, géneros, radio, pausar, reanudar, siguiente pista, subir o bajar volumen.\n"
    "- Herramientas prácticas: poner alarmas, temporizadores, recordatorios, listas de la compra, operaciones matemáticas y conversiones de unidades o moneda.\n"
    "- Comandos breves y directos de control: \"silencio\", \"para\", \"cancela\", \"apaga todo\", \"hola\", \"buenos días\", \"gracias\".\n\n"
    "CRITERIOS PARA \"NO\" (RECHAZAR - ACTIVACIÓN ACCIDENTAL O RUIDO):\n"
    "- Conversaciones entre personas en la habitación o peticiones entre humanos: \"mamá pásame el agua\", \"oye cariño\", \"le dije a Juan que no\", \"pásame la sal\".\n"
    "- Audio proveniente de televisión, noticias, partidos de fútbol, películas, series o podcasts: \"el árbitro pitó penalti\", \"según el telediario\", \"los sondeos electorales\".\n"
    "- Historias o relatos personales en tiempo pasado: \"ayer estuve en el trabajo\", \"cuando llegamos al hotel\".\n"
    "- Frases incompletas, muletillas, ruidos vocales o divagaciones: \"y entonces bueno...\", \"pero es que claro\".\n\n"
    "Responde ÚNICAMENTE con la palabra \"SI\" o \"NO\". Ninguna otra palabra."
)

CONF_SILENT_DISCARD = "silent_discard"
DEFAULT_SILENT_DISCARD = True
