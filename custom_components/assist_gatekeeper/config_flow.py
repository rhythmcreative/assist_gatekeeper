"""Config flow for Assist Gatekeeper."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

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


class AssistGatekeeperConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Assist Gatekeeper."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title="Assist Gatekeeper", data=user_input
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_OLLAMA_URL, default=DEFAULT_OLLAMA_URL): str,
                vol.Required(
                    CONF_VERIFIER_MODEL, default=DEFAULT_VERIFIER_MODEL
                ): str,
                vol.Required(
                    CONF_TARGET_AGENT, default=DEFAULT_TARGET_AGENT
                ): str,
                vol.Required(
                    CONF_ENABLE_HEURISTICS, default=DEFAULT_ENABLE_HEURISTICS
                ): bool,
                vol.Required(
                    CONF_SILENT_DISCARD, default=DEFAULT_SILENT_DISCARD
                ): bool,
                vol.Required(
                    CONF_VERIFIER_PROMPT, default=DEFAULT_VERIFIER_PROMPT
                ): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return AssistGatekeeperOptionsFlowHandler()


class AssistGatekeeperOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Assist Gatekeeper."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        conf = {**self.config_entry.data, **self.config_entry.options}

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_OLLAMA_URL,
                    default=conf.get(CONF_OLLAMA_URL, DEFAULT_OLLAMA_URL),
                ): str,
                vol.Required(
                    CONF_VERIFIER_MODEL,
                    default=conf.get(
                        CONF_VERIFIER_MODEL, DEFAULT_VERIFIER_MODEL
                    ),
                ): str,
                vol.Required(
                    CONF_TARGET_AGENT,
                    default=conf.get(CONF_TARGET_AGENT, DEFAULT_TARGET_AGENT),
                ): str,
                vol.Required(
                    CONF_ENABLE_HEURISTICS,
                    default=conf.get(
                        CONF_ENABLE_HEURISTICS, DEFAULT_ENABLE_HEURISTICS
                    ),
                ): bool,
                vol.Required(
                    CONF_SILENT_DISCARD,
                    default=conf.get(
                        CONF_SILENT_DISCARD, DEFAULT_SILENT_DISCARD
                    ),
                ): bool,
                vol.Required(
                    CONF_VERIFIER_PROMPT,
                    default=conf.get(
                        CONF_VERIFIER_PROMPT, DEFAULT_VERIFIER_PROMPT
                    ),
                ): str,
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
