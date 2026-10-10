# Support Ticket Triage

An LLM-powered classifier that turns a raw customer message into **structured, validated JSON**: a category, a confidence score, and a short suggested reply.

Built with the **Groq API** (OpenAI-compatible endpoint), prompt engineering, and **Pydantic** schema validation.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Groq](https://img.shields.io/badge/LLM-Groq-orange.svg)
![Pydantic](https://img.shields.io/badge/validation-Pydantic-e92063.svg)

---

## Features

- **Structured output**: the model is forced into JSON mode (`response_format={"type": "json_object"}`).
- **Schema validation**: the response is parsed and validated with Pydantic (`category`, `confidence` in `[0, 1]`, `answer`) before being shown.
- **Input guardrails**: rejects empty messages and messages over 1000 characters.
- **Prompt-injection resistance**: the system prompt instructs the model to treat user messages as data, not instructions.
- **Prompt kept separate from code**: the system prompt lives in `prompts/system_prompt.txt`, so it can be iterated without touching Python.

## How it works

```
 user message
      │
      ▼
 validate_input()  ──► empty / >1000 chars → ValueError
      │
      ▼
 classify_message() ──► Groq (openai/gpt-oss-20b) + system prompt, JSON mode
      │
      ▼
 Pydantic Classification.model_validate()
      │
      ▼
 validated JSON result
```

## Project structure

```
support-ticket-triage/
├── prompts/
│   └── system_prompt.txt   # classifier instructions + few-shot example
├── main.py                 # CLI entry point, guardrails, LLM call, validation
├── requirements.txt
├── .env.example
└── .gitignore
```

## Getting started

### 1. Clone and install

```bash
git clone https://github.com/muhammed-alaa74/support-ticket-triage.git
cd support-ticket-triage

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure your API key

Get a free key from the [Groq Console](https://console.groq.com/keys), then:

```bash
cp .env.example .env
```

Edit `.env` and set your key:

```env
OPENAI_API_KEY=your_groq_api_key_here
```

> The variable is named `OPENAI_API_KEY` because the app uses the OpenAI Python SDK pointed at Groq's OpenAI-compatible endpoint. The value must be your **Groq** key.

### 3. Run

```bash
python main.py
```

## Example

```text
Enter a customer message: My payment was charged twice.

Result:
{
  "category": "billing",
  "confidence": 0.95,
  "answer": "Please contact billing support."
}
```

## Output schema

| Field        | Type    | Description                                      |
| ------------ | ------- | ------------------------------------------------ |
| `category`   | string  | One of `technical`, `billing`, `general`         |
| `confidence` | float   | Model confidence, between `0` and `1`            |
| `answer`     | string  | Short suggested response for the customer        |

## Guardrails

| Layer  | Check                                                           |
| ------ | --------------------------------------------------------------- |
| Input  | Non-empty, max 1000 characters                                  |
| Prompt | User text treated as data, not instructions                     |
| Output | JSON mode + Pydantic validation (type and `0 ≤ confidence ≤ 1`) |

## Configuration

| Setting  | Where                            | Default                  |
| -------- | -------------------------------- | ------------------------ |
| Model    | `classify_message()` in `main.py`| `openai/gpt-oss-20b`     |
| Base URL | `classify_message()` in `main.py`| `https://api.groq.com/openai/v1` |
| Prompt   | `prompts/system_prompt.txt`      | 3 categories + 1 example |

## Roadmap

- [ ] Restrict `category` to an `Enum` / `Literal` in the Pydantic model
- [ ] Retry on invalid JSON
- [ ] Batch mode (CSV in, CSV out)
- [ ] Evaluation set with accuracy metrics
- [ ] REST API wrapper (FastAPI)

## Tech stack

Python · Groq API · OpenAI SDK · Pydantic · python-dotenv