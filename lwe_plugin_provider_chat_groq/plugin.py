"""LWE chat groq provider integration."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from groq import Groq
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from pydantic import Field
from typing_extensions import override

from lwe.core.config import Config
from lwe.core.provider import PresetValue, Provider

CHAT_GROQ_DEFAULT_MODEL = "llama3-8b-8192"


class CustomChatGroq(ChatGroq):

    model_name: str = Field(alias="model", default=CHAT_GROQ_DEFAULT_MODEL)
    """Model name to use."""

    @property
    @override
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "chat_groq"


class ProviderChatGroq(Provider):
    """
    Access to Groq chat models.
    """

    def __init__(self, config: Config | None = None, **kwargs: Any) -> None:
        super().__init__(config, **kwargs)
        self.show_inactive_models: bool = bool(
            self.config.get("plugins.provider_chat_groq.show_inactive_models", False)
        )

    def fetch_models(self) -> dict[str, dict[str, int | None]]:
        client = Groq()
        try:
            models_list = client.models.list()
            models = {
                model.id: {"max_tokens": model.model_extra.get("context_window")}
                for model in models_list.data
                if model.model_extra is not None
                and (self.show_inactive_models or model.model_extra.get("active"))
            }
            return models
        except Exception as e:
            raise ValueError(f"Could not retrieve models: {e}")

    @property
    @override
    def capabilities(self) -> dict[str, bool]:
        return {
            "chat": True,
            "validate_models": True,
        }

    @property
    @override
    def default_model(self) -> str:
        return CHAT_GROQ_DEFAULT_MODEL

    @override
    def prepare_messages_method(
        self,
    ) -> Callable[[list[dict[str, Any]]], list[BaseMessage]]:
        return self.prepare_messages_for_llm_chat

    @override
    def llm_factory(self) -> type[CustomChatGroq]:
        return CustomChatGroq

    @override
    def customization_config(self) -> dict[str, Any]:
        return {
            "model_name": PresetValue(str, options=self.available_models),
            "temperature": PresetValue(float, min_value=0.0, max_value=2.0),
            "max_tokens": PresetValue(int, include_none=True),
            "top_p": PresetValue(float, min_value=0.0, max_value=1.0),
            "tools": None,
            "tool_choice": None,
        }
