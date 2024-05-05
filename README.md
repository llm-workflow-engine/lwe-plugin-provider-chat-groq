# LLM Workflow Engine (LWE) Chat Groq Provider plugin

Chat Groq Provider plugin for [LLM Workflow Engine](https://github.com/llm-workflow-engine/llm-workflow-engine)

Access to [Groq](https://console.groq.com/docs/models) chat models.

## Installation

### From packages

Install the latest version of this software directly from github with pip:

```bash
pip install git+https://github.com/llm-workflow-engine/lwe-plugin-provider-chat-groq
```

### From source (recommended for development)

Install the latest version of this software directly from git:

```bash
git clone https://github.com/llm-workflow-engine/lwe-plugin-provider-chat-groq.git
```

Install the development package:

```bash
cd lwe-plugin-provider-chat-groq
pip install -e .
```

## Configuration

Add the following to `config.yaml` in your profile:

```yaml
plugins:
  enabled:
    - provider_chat_groq
    # Any other plugins you want enabled...
  # THIS IS OPTIONAL -- By default the plugin loads all model data via an API
  # call on startup. This does make startup time longer.
  # You can instead provide a 'models' object here with the relevant data, and
  # It will be used instead of an API call.
  provider_chat_groq:
    # Set to True to show inactive models.
    show_inactive_models: False
    models:
      # 'id' parameter of the model as it appears in the API.
      mixtral-8x7b-32768:
        # The only parameter, and it's required.
        max_tokens: 32768
```

## Usage

From a running LWE shell:

```
/provider chat_groq
/model model_name mixtral-8x7b-32768
```
