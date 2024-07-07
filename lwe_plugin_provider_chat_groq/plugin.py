from groq import Groq
from langchain_groq import ChatGroq

from lwe.core.provider import Provider, PresetValue

CHAT_GROQ_DEFAULT_MODEL = "mixtral-8x7b-32768"


class CustomChatGroq(ChatGroq):

    @property
    def _llm_type(self):
        """Return type of llm."""
        return "chat_groq"


class ProviderChatGroq(Provider):
    """
    Access to Groq chat models.
    """

    def __init__(self, config=None, **kwargs):
        super().__init__(config, **kwargs)
        self.show_inactive_models = self.config.get('plugins.provider_chat_groq.show_inactive_models', False)

    def fetch_models(self):
        client = Groq()
        try:
            models_list = client.models.list()
            models = {model.id: {'max_tokens': model.context_window} for model in models_list.data if (self.show_inactive_models or model.active)}
            return models
        except Exception as e:
            raise ValueError(f"Could not retrieve models: {e}")

    @property
    def capabilities(self):
        return {
            "chat": True,
            'validate_models': True,
        }

    @property
    def default_model(self):
        return CHAT_GROQ_DEFAULT_MODEL

    def prepare_messages_method(self):
        return self.prepare_messages_for_llm_chat

    def llm_factory(self):
        return CustomChatGroq

    def customization_config(self):
        return {
            'model_name': PresetValue(str, options=self.available_models),
            'temperature': PresetValue(float, min_value=0.0, max_value=2.0),
            'max_tokens': PresetValue(int, include_none=True),
            'top_p': PresetValue(float, min_value=0.0, max_value=1.0),
            "tools": None,
            "tool_choice": None,
        }
