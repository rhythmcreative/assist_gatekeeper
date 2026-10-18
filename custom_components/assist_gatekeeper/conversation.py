"""Conversation agent platform for Assist Gatekeeper."""

from __future__ import annotations

import logging
import re
from typing import Literal

import aiohttp
from homeassistant.components import conversation
from homeassistant.components.conversation import (
    AbstractConversationAgent,
    ConversationEntity,
    ConversationInput,
    ConversationResult,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_ENABLE_HEURISTICS,
    CONF_OLLAMA_URL,
    CONF_SILENT_DISCARD,
    CONF_TARGET_AGENT,
    CONF_VERIFIER_MODEL,
    CONF_VERIFIER_PROMPT,
    DEFAULT_ENABLE_HEURISTICS,
    DEFAULT_OLLAMA_URL,
    DEFAULT_SILENT_DISCARD,
    DEFAULT_TARGET_AGENT,
    DEFAULT_VERIFIER_MODEL,
    DEFAULT_VERIFIER_PROMPT,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

# Common STT garbage / hallucination fragments to discard instantly without LLM
COMMON_NOISE_FRAGMENTS = {
    "",
    "eh",
    "ah",
    "uh",
    "um",
    "hmm",
    "...",
    "subtítulos realizados por la comunidad de amara.org",
    "gracias por ver el video",
    "suscríbete al canal",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Assist Gatekeeper conversation entity."""
    async_add_entities([AssistGatekeeperEntity(hass, entry)])


class AssistGatekeeperEntity(ConversationEntity, AbstractConversationAgent):
    """Gatekeeper Conversation Agent that validates turns before delegating."""

    _attr_has_entity_name = True
    _attr_name = "Assist Gatekeeper"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the gatekeeper entity."""
        self.hass = hass
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_gatekeeper"

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return supported languages."""
        return MATCH_ALL

    async def async_added_to_hass(self) -> None:
        """Register the agent when added to Home Assistant."""
        await super().async_added_to_hass()
        conversation.async_set_agent(self.hass, self.entry, self)

    async def async_will_remove_from_hass(self) -> None:
        """Unregister the agent when removed."""
        conversation.async_unset_agent(self.hass, self.entry)
        await super().async_will_remove_from_hass()

    async def async_process(
        self, user_input: ConversationInput
    ) -> ConversationResult:
        """Process turn: verify intent before calling the primary LLM."""
        conf = {**self.entry.data, **(self.entry.options or {})}
        ollama_url = conf.get(CONF_OLLAMA_URL, DEFAULT_OLLAMA_URL).rstrip("/")
        verifier_model = conf.get(CONF_VERIFIER_MODEL, DEFAULT_VERIFIER_MODEL)
        target_agent = conf.get(CONF_TARGET_AGENT, DEFAULT_TARGET_AGENT)
        enable_heuristics = conf.get(
            CONF_ENABLE_HEURISTICS, DEFAULT_ENABLE_HEURISTICS
        )
        verifier_prompt = conf.get(
            CONF_VERIFIER_PROMPT, DEFAULT_VERIFIER_PROMPT
        )
        silent_discard = conf.get(CONF_SILENT_DISCARD, DEFAULT_SILENT_DISCARD)

        text = (user_input.text or "").strip()

        # Step 1: Immediate Heuristic Fast Filter
        if enable_heuristics:
            clean_lower = re.sub(r"[^\w\s]", "", text.lower()).strip()
            if not clean_lower or clean_lower in COMMON_NOISE_FRAGMENTS or len(clean_lower) < 2:
                _LOGGER.info("🛡️ [Gatekeeper DROP] Ignored empty or noise input: '%s'", text)
                return self._build_silent_response(user_input, silent_discard)

        # Step 2: Ultra-Fast LLM Pre-Flight Check (Gemma 2B)
        is_valid = await self._verify_intent(
            ollama_url=ollama_url,
            model=verifier_model,
            system_prompt=verifier_prompt,
            text=text,
        )

        if not is_valid:
            _LOGGER.info(
                "🛡️ [Gatekeeper REJECTED] Accidental background/TV trigger: '%s'",
                text,
            )
            return self._build_silent_response(user_input, silent_discard)

        # Step 3: Verified Intent -> Transparently Forward to Main Conversation Agent
        _LOGGER.info(
            "🛡️ [Gatekeeper ACCEPTED] Verified command: '%s' -> Forwarding to %s",
            text,
            target_agent,
        )

        try:
            return await conversation.async_converse(
                hass=self.hass,
                text=text,
                conversation_id=user_input.conversation_id,
                context=user_input.context,
                agent_id=target_agent,
                device_id=user_input.device_id,
                extra_system_prompt=user_input.extra_system_prompt,
            )
        except Exception as err:
            _LOGGER.error("Error delegating to target agent %s: %s", target_agent, err)
            resp = intent.IntentResponse(language=user_input.language)
            resp.async_set_speech("Error al conectar con el asistente principal.")
            return ConversationResult(
                response=resp,
                conversation_id=user_input.conversation_id,
            )

    async def _verify_intent(
        self,
        ollama_url: str,
        model: str,
        system_prompt: str,
        text: str,
    ) -> bool:
        """Call fast pre-flight verifier model to classify turn."""
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f'Frase: "{text}"'},
            ],
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_predict": 3,
            },
        }

        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=3.0)
            ) as session:
                async with session.post(
                    f"{ollama_url}/api/chat", json=payload
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        reply = (
                            data.get("message", {}).get("content") or ""
                        ).strip().upper()
                        # If reply contains 'SI', it is a valid intentional command
                        return "SI" in reply
                    else:
                        _LOGGER.warning(
                            "Verifier endpoint returned HTTP %s, failing open to prevent blocking",
                            resp.status,
                        )
                        return True
        except Exception as err:
            _LOGGER.warning("Verifier check failed (%s), failing open", err)
            return True

    def _build_silent_response(
        self, user_input: ConversationInput, silent: bool
    ) -> ConversationResult:
        """Build an empty silent response to dismiss satellite cleanly."""
        intent_resp = intent.IntentResponse(language=user_input.language)
        if not silent:
            intent_resp.async_set_speech("Ignorado.")
        else:
            intent_resp.response_type = intent.IntentResponseType.ACTION_DONE
        return ConversationResult(
            response=intent_resp,
            conversation_id=user_input.conversation_id,
        )
