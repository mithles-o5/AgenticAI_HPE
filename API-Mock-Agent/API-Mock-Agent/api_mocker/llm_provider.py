"""
api_mocker/llm_provider.py
Multi-provider LLM factory — supports free and paid backends.

Supported providers (in recommended order for free usage):
──────────────────────────────────────────────────────────
  groq        FREE — Llama 3, Mixtral on Groq Cloud (fast, generous free tier)
              Env: GROQ_API_KEY  (get free at https://console.groq.com)

  gemini      FREE — Google Gemini via AI Studio (generous free tier)
              Env: GOOGLE_API_KEY  (get free at https://aistudio.google.com/apikey)

  ollama      FREE — 100% local, no API key needed (requires Ollama installed)
              Install: https://ollama.com  then  `ollama pull llama3.1`

  huggingface FREE — HuggingFace Inference API (rate-limited free tier)
              Env: HUGGINGFACEHUB_API_TOKEN  (get free at https://huggingface.co/settings/tokens)

  anthropic   PAID — Claude Sonnet (best quality, costs money)
              Env: ANTHROPIC_API_KEY

Usage:
    from api_mocker.llm_provider import create_llm
    llm = create_llm("groq")          # Uses GROQ_API_KEY from env
    llm = create_llm("gemini")        # Uses GOOGLE_API_KEY from env
    llm = create_llm("ollama")        # Connects to local Ollama
    llm = create_llm()                # Auto-detects from available keys
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from langchain_core.language_models.chat_models import BaseChatModel

logger = logging.getLogger(__name__)

# ── Provider registry ────────────────────────────────────────────────────────

# (provider_name, env_var_needed, display_name, signup_url)
PROVIDERS = [
    ("groq",        "GROQ_API_KEY",             "Groq (Llama 3 — FREE)",          "https://console.groq.com"),
    ("gemini",      "GOOGLE_API_KEY",           "Google Gemini (FREE)",            "https://aistudio.google.com/apikey"),
    ("ollama",      None,                        "Ollama (local — FREE)",           "https://ollama.com"),
    ("huggingface", "HUGGINGFACEHUB_API_TOKEN", "HuggingFace Inference (FREE)",    "https://huggingface.co/settings/tokens"),
    ("anthropic",   "ANTHROPIC_API_KEY",        "Anthropic Claude (PAID)",         "https://console.anthropic.com"),
]


def list_providers() -> str:
    """Return a formatted table of all supported providers."""
    lines = [
        "\n  Supported LLM Providers:",
        "  ┌────────────────┬──────────────────────────────┬────────────────────────────────────────┐",
        "  │  Provider      │  Key env var                 │  Status                                │",
        "  ├────────────────┼──────────────────────────────┼────────────────────────────────────────┤",
    ]
    for name, env_var, display, url in PROVIDERS:
        if env_var is None:
            status = "no key needed"
        elif os.getenv(env_var):
            status = "✅ key found"
        else:
            status = f"❌ set {env_var}"
        lines.append(f"  │  {name:<12}  │  {(env_var or 'none'):<28}│  {status:<38}│")
    lines.append(
        "  └────────────────┴──────────────────────────────┴────────────────────────────────────────┘"
    )
    return "\n".join(lines)


# ── Factory ──────────────────────────────────────────────────────────────────


def create_llm(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    max_tokens: int = 16384,
    temperature: float = 0.0,
) -> BaseChatModel:
    """
    Create a LangChain chat model for the given provider.

    If provider is None, auto-detects the best available free provider.
    """

    if provider is None:
        provider = _auto_detect_provider()

    provider = provider.lower().strip()

    if provider == "groq":
        return _create_groq(model, max_tokens, temperature)
    elif provider == "gemini":
        return _create_gemini(model, max_tokens, temperature)
    elif provider == "ollama":
        return _create_ollama(model, max_tokens, temperature)
    elif provider == "huggingface":
        return _create_huggingface(model, max_tokens, temperature)
    elif provider == "anthropic":
        return _create_anthropic(model, max_tokens, temperature)
    else:
        raise ValueError(
            f"Unknown provider: '{provider}'. "
            f"Supported: groq, gemini, ollama, huggingface, anthropic"
        )


# ── Auto-detection ───────────────────────────────────────────────────────────


def _auto_detect_provider() -> str:
    """Pick the best available provider based on env vars present."""
    # Priority: groq (fastest free) → gemini → huggingface → ollama → anthropic
    if os.getenv("GROQ_API_KEY"):
        logger.info("Auto-detected GROQ_API_KEY → using Groq (free)")
        return "groq"
    if os.getenv("GOOGLE_API_KEY"):
        logger.info("Auto-detected GOOGLE_API_KEY → using Google Gemini (free)")
        return "gemini"
    if os.getenv("HUGGINGFACEHUB_API_TOKEN"):
        logger.info("Auto-detected HUGGINGFACEHUB_API_TOKEN → using HuggingFace (free)")
        return "huggingface"
    if os.getenv("ANTHROPIC_API_KEY"):
        logger.info("Auto-detected ANTHROPIC_API_KEY → using Anthropic (paid)")
        return "anthropic"
    # Default to Ollama (local, no key needed)
    logger.info("No API keys found → falling back to Ollama (local, free)")
    return "ollama"


def _check_key(env_var: str, provider_name: str) -> str:
    key = os.getenv(env_var, "")
    if not key:
        raise ValueError(
            f"\n  ❌  {env_var} is not set!\n"
            f"  To use {provider_name}, get a FREE key and set it:\n"
            f"    export {env_var}=your-key-here\n"
            f"  Or add it to your .env file.\n"
        )
    return key


# ── Provider implementations ─────────────────────────────────────────────────


def _create_groq(
    model: Optional[str], max_tokens: int, temperature: float
) -> BaseChatModel:
    """
    Groq — FREE tier with generous limits.
    Models: llama-3.3-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b-32768
    Sign up: https://console.groq.com
    """
    from langchain_groq import ChatGroq

    key = _check_key("GROQ_API_KEY", "Groq")
    model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    logger.info(f"Using Groq: {model} (FREE)")
    return ChatGroq(
        model=model,
        api_key=key,
        max_tokens=max_tokens,
        temperature=temperature,
    )


def _create_gemini(
    model: Optional[str], max_tokens: int, temperature: float
) -> BaseChatModel:
    """
    Google Gemini — FREE tier via AI Studio.
    Models: gemini-2.0-flash, gemini-1.5-flash, gemini-1.5-pro
    Sign up: https://aistudio.google.com/apikey
    """
    from langchain_google_genai import ChatGoogleGenerativeAI

    key = _check_key("GOOGLE_API_KEY", "Google Gemini")
    model = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    logger.info(f"Using Google Gemini: {model} (FREE)")
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=key,
        max_output_tokens=max_tokens,
        temperature=temperature,
    )


def _create_ollama(
    model: Optional[str], max_tokens: int, temperature: float
) -> BaseChatModel:
    """
    Ollama — 100% local, no API key, completely FREE.
    Requires Ollama installed: https://ollama.com
    Then: ollama pull llama3.1
    """
    from langchain_ollama import ChatOllama

    model = model or os.getenv("OLLAMA_MODEL", "llama3.1")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    logger.info(f"Using Ollama (local): {model} at {base_url} (FREE)")
    return ChatOllama(
        model=model,
        base_url=base_url,
        num_predict=max_tokens,
        temperature=temperature,
    )


def _create_huggingface(
    model: Optional[str], max_tokens: int, temperature: float
) -> BaseChatModel:
    """
    HuggingFace Inference API — FREE tier (rate-limited).
    Uses the HF Router with OpenAI-compatible chat completions endpoint.
    Sign up: https://huggingface.co/settings/tokens
    """
    from langchain_openai import ChatOpenAI

    key = _check_key("HUGGINGFACEHUB_API_TOKEN", "HuggingFace")
    model = model or os.getenv("HF_MODEL", "meta-llama/llama-3.1-8b-instruct")
    logger.info(f"Using HuggingFace: {model} (FREE)")

    # HuggingFace Router exposes an OpenAI-compatible endpoint
    # Cap max_tokens to stay within the model's context window
    return ChatOpenAI(
        model=model,
        api_key=key,
        base_url="https://router.huggingface.co/novita/v3/openai",
        max_tokens=min(max_tokens, 2048),
        temperature=max(temperature, 0.01),
        timeout=120,  # Free tier can be slow
    )


def _create_anthropic(
    model: Optional[str], max_tokens: int, temperature: float
) -> BaseChatModel:
    """
    Anthropic Claude — PAID, best quality.
    """
    from langchain_anthropic import ChatAnthropic

    key = _check_key("ANTHROPIC_API_KEY", "Anthropic")
    model = model or os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
    logger.info(f"Using Anthropic: {model} (PAID)")
    return ChatAnthropic(
        model=model,
        api_key=key,
        max_tokens=max_tokens,
        temperature=temperature,
    )
