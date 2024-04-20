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

    @property
    def capabilities(self):
        return {
            "chat": True,
            'validate_models': True,
            'models': {
                'llama2-70b-4096': {
                    'max_tokens': 4096,
                },
                'gemma-7b-it': {
                    'max_tokens': 8192,
                },
                'mixtral-8x7b-32768': {
                    'max_tokens': 32768,
                },
                'llama3-8b-8192': {
                    'max_tokens': 8192,
                },
                'llama3-70b-8192': {
                    'max_tokens': 8192,
                },
            }
        }

    @property
    def default_model(self):
        return CHAT_GROQ_DEFAULT_MODEL

    def llm_factory(self):
        return CustomChatGroq

    def customization_config(self):
        return {
            'model_name': PresetValue(str, options=self.available_models),
            'temperature': PresetValue(float, min_value=0.0, max_value=2.0),
            'max_tokens': PresetValue(int, include_none=True),
            'top_p': PresetValue(float, min_value=0.0, max_value=1.0),
        }
