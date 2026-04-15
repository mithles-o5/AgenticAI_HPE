"""
com_mock/llm_provider.py
─────────────────────────
Multi-provider LLM factory.
Supports: groq (FREE), gemini (FREE), ollama (local/FREE),
          huggingface (FREE), anthropic (paid).
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from langchain_core.language_models.chat_models import BaseChatModel

logger = logging.getLogger(__name__)

PROVIDERS = [
    ("groq",        "GROQ_API_KEY",             "Groq Llama3 (FREE)",       "https://console.groq.com"),
    ("gemini",      "GOOGLE_API_KEY",            "Google Gemini (FREE)",     "https://aistudio.google.com/apikey"),
    ("ollama",      None,                         "Ollama local (FREE)",      "https://ollama.com"),
    ("huggingface", "HUGGINGFACEHUB_API_TOKEN",  "HuggingFace (FREE)",       "https://huggingface.co/settings/tokens"),
    ("anthropic",   "ANTHROPIC_API_KEY",         "Anthropic Claude (PAID)",  "https://console.anthropic.com"),
]


def list_providers() -> str:
    lines = [
        "\n  LLM Providers:",
        "  ┌─────────────┬──────────────────────────────┬───────────────────┐",
        "  │ Provider    │ Env var                      │ Status            │",
        "  ├─────────────┼──────────────────────────────┼───────────────────┤",
    ]
    for name, env, display, _ in PROVIDERS:
        if env is None:
            status = "no key needed"
        elif os.getenv(env):
            status = "✅ key found"
        else:
            status = f"❌ set {env}"
        lines.append(f"  │ {name:<11} │ {(env or 'none'):<28} │ {status:<17} │")
    lines.append("  └─────────────┴──────────────────────────────┴───────────────────┘")
    return "\n".join(lines)


def create_llm(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    max_tokens: int = 16384,
    temperature: float = 0.0,
) -> BaseChatModel:
    if provider is None:
        provider = _auto_detect()

    provider = provider.lower().strip()
    if provider == "groq":
        return _groq(model, max_tokens, temperature)
    elif provider == "gemini":
        return _gemini(model, max_tokens, temperature)
    elif provider == "ollama":
        return _ollama(model, max_tokens, temperature)
    elif provider == "huggingface":
        return _huggingface(model, max_tokens, temperature)
    elif provider == "anthropic":
        return _anthropic(model, max_tokens, temperature)
    else:
        raise ValueError(f"Unknown provider: '{provider}'")


def _auto_detect() -> str:
    if os.getenv("GROQ_API_KEY"):
        logger.info("Auto-detected GROQ_API_KEY → groq")
        return "groq"
    if os.getenv("GOOGLE_API_KEY"):
        logger.info("Auto-detected GOOGLE_API_KEY → gemini")
        return "gemini"
    if os.getenv("HUGGINGFACEHUB_API_TOKEN"):
        return "huggingface"
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    logger.info("No keys found → falling back to Ollama")
    return "ollama"


def _key(env: str, name: str) -> str:
    k = os.getenv(env, "")
    if not k:
        raise ValueError(f"❌ {env} not set. Set it to use {name}.")
    return k


def _groq(model, max_tokens, temperature):
    from langchain_groq import ChatGroq
    key = _key("GROQ_API_KEY", "Groq")
    model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    logger.info("LLM: Groq %s (FREE)", model)
    return ChatGroq(model=model, api_key=key, max_tokens=max_tokens, temperature=temperature)


def _gemini(model, max_tokens, temperature):
    from langchain_google_genai import ChatGoogleGenerativeAI
    key = _key("GOOGLE_API_KEY", "Gemini")
    model = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    logger.info("LLM: Gemini %s (FREE)", model)
    return ChatGoogleGenerativeAI(model=model, google_api_key=key,
                                   max_output_tokens=max_tokens, temperature=temperature)


def _ollama(model, max_tokens, temperature):
    from langchain_ollama import ChatOllama
    model = model or os.getenv("OLLAMA_MODEL", "llama3.1")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    logger.info("LLM: Ollama %s at %s (FREE)", model, base_url)
    return ChatOllama(model=model, base_url=base_url, num_predict=max_tokens, temperature=temperature)


def _huggingface(model, max_tokens, temperature):
    from langchain_openai import ChatOpenAI
    key = _key("HUGGINGFACEHUB_API_TOKEN", "HuggingFace")
    model = model or os.getenv("HF_MODEL", "meta-llama/llama-3.1-8b-instruct")
    logger.info("LLM: HuggingFace %s (FREE)", model)
    return ChatOpenAI(model=model, api_key=key,
                      base_url="https://router.huggingface.co/novita/v3/openai",
                      max_tokens=min(max_tokens, 2048),
                      temperature=max(temperature, 0.01), timeout=120)


def _anthropic(model, max_tokens, temperature):
    from langchain_anthropic import ChatAnthropic
    key = _key("ANTHROPIC_API_KEY", "Anthropic")
    model = model or os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
    logger.info("LLM: Anthropic %s (PAID)", model)
    return ChatAnthropic(model=model, api_key=key, max_tokens=max_tokens, temperature=temperature)
