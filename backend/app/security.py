"""
security.py — FarmaSense AI Security Layer
Covers:
  1. Per-user rate limiting (in-memory token bucket, no Redis dep)
  2. Input sanitization & prompt injection defense
  3. LLM output schema validation before MongoDB storage
"""
import re
import time
import html
from collections import defaultdict
from threading import Lock
from functools import wraps
from flask import jsonify, current_app
from flask_jwt_extended import get_jwt_identity

# ─────────────────────────────────────────────
# 1. RATE LIMITER  (Token Bucket, per user_id)
# ─────────────────────────────────────────────
_rate_store: dict = defaultdict(lambda: {"tokens": 0.0, "last": time.time()})
_rate_lock  = Lock()

def _check_rate_limit(user_id: str, max_per_minute: int = 5) -> bool:
    """Returns True if the request is ALLOWED, False if throttled."""
    refill_rate = max_per_minute / 60.0   # tokens per second
    capacity    = float(max_per_minute)

    with _rate_lock:
        bucket = _rate_store[user_id]
        now    = time.time()
        elapsed = now - bucket["last"]

        # Refill bucket
        bucket["tokens"] = min(capacity, bucket["tokens"] + elapsed * refill_rate)
        bucket["last"]   = now

        if bucket["tokens"] >= 1.0:
            bucket["tokens"] -= 1.0
            return True   # allowed
        return False      # throttled


def ai_rate_limit(max_per_minute: int = 5):
    """
    Decorator — apply to AI endpoints.
    Default: 5 calls/min per user. Adjust per endpoint as needed.

    Usage:
        @advisory_bp.route("/generate", methods=["POST"])
        @jwt_required()
        @ai_rate_limit(max_per_minute=3)
        def generate(): ...
    """
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            # Bypass rate limiting during unit tests
            if current_app.config.get("TESTING"):
                return await fn(*args, **kwargs)

            user_id = str(get_jwt_identity())
            if not _check_rate_limit(user_id, max_per_minute):
                return jsonify({
                    "error": "Too many requests. Please wait before generating again.",
                    "retry_in": "60 seconds"
                }), 429
            return await fn(*args, **kwargs)
        return wrapper
    return decorator


# ─────────────────────────────────────────────
# 2. INPUT SANITIZATION + PROMPT INJECTION DEFENSE
# ─────────────────────────────────────────────

# Known prompt injection patterns — intentionally kept readable
_INJECTION_PATTERNS = [
    # Role hijacking
    r"ignore (all )?(previous|prior|above) (instructions?|prompts?|context)",
    r"you are now",
    r"forget (everything|your instructions?|above)",
    r"act as (a |an )?(different|new|another)",
    r"disregard your",
    r"pretend (you are|to be)",
    r"do not follow",
    r"override (previous|system)",
    # Jailbreaks
    r"jailbreak",
    r"DAN mode",
    r"developer mode",
    r"unrestricted mode",
    # Data exfiltration attempts
    r"reveal (your |the )?(system prompt|instructions?|api key|secret)",
    r"print (your|the) (system|prompt|instructions?)",
    r"what (is|are) your (instructions?|prompt|system)",
    # Direct instruction overrides
    r"instead,? (do|be|say|output|write|return)",
    r"now (do|say|ignore|forget|be)",
]
_COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in _INJECTION_PATTERNS]

# Allowed languages — prevents free-text injection via the language field
ALLOWED_LANGUAGES = {
    "English", "Hindi", "Bengali", "Telugu", "Marathi", "Tamil",
    "Urdu", "Gujarati", "Kannada", "Odia", "Punjabi", "Malayalam", "Assamese"
}


def sanitize_user_input(text: str, max_length: int = 500) -> tuple[str, str | None]:
    """
    Cleans and validates raw user input.
    Returns (cleaned_text, error_message_or_None).
    If error is returned, the caller should reject the request.
    """
    if not text or not isinstance(text, str):
        return "", "Input must be a non-empty string."

    # Strip HTML entities and leading/trailing whitespace
    text = html.unescape(text).strip()

    # Hard length cap
    if len(text) > max_length:
        return "", f"Input too long. Maximum {max_length} characters allowed."

    # Block null bytes and ASCII control characters (except newline/tab)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Detect prompt injection
    for pattern in _COMPILED_PATTERNS:
        if pattern.search(text):
            return "", "Invalid input: restricted content detected."

    return text, None


def validate_language(language: str) -> tuple[str, str | None]:
    """
    Checks that language is one of the supported values.
    Returns (language, error_or_None).
    """
    if language not in ALLOWED_LANGUAGES:
        return "English", f"Unsupported language '{language}'. Defaulting to English."
    return language, None


# ─────────────────────────────────────────────
# 3. LLM OUTPUT SCHEMA VALIDATION
# ─────────────────────────────────────────────

ADVISORY_SCHEMA = {
    "season"             : str,
    "recommended_crop"   : str,
    "second_option_crop" : str,
    "avoid_crop"         : str,
    "expected_profit_min": (int, float),
    "expected_profit_max": (int, float),
    "confidence_score"   : (int, float),
    "final_advisory"     : str,
}

_MAX_STRING_LENGTH = 3000   # cap any single string field from LLM

def validate_advisory_output(data: dict) -> tuple[dict, list[str]]:
    """
    Validates and sanitizes the advisory dict returned by the LLM.
    Returns (sanitized_data, list_of_warnings).
    Fills in safe defaults for missing/wrong-typed fields rather than crashing.
    """
    warnings = []
    sanitized = {}

    for key, expected_type in ADVISORY_SCHEMA.items():
        value = data.get(key)
        if value is None:
            warnings.append(f"Missing field: '{key}' — using default.")
            # Provide a safe default
            sanitized[key] = "" if expected_type is str else 0
            continue

        if not isinstance(value, expected_type):
            warnings.append(f"Wrong type for '{key}': got {type(value).__name__}, expected {expected_type}. Coercing.")
            try:
                if expected_type is str:
                    value = str(value)
                elif expected_type in ((int, float), (float, int)):
                    value = float(value)
                else:
                    value = expected_type(value)
            except (ValueError, TypeError):
                value = "" if expected_type is str else 0

        # Cap strings to prevent oversized documents
        if isinstance(value, str):
            if len(value) > _MAX_STRING_LENGTH:
                warnings.append(f"Field '{key}' truncated to {_MAX_STRING_LENGTH} chars.")
                value = value[:_MAX_STRING_LENGTH]
            # Strip control characters from LLM string output
            value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", value)

        # Clamp numeric ranges
        if key == "confidence_score" and isinstance(value, (int, float)):
            value = max(0.0, min(1.0, float(value)))

        if key in ("expected_profit_min", "expected_profit_max") and isinstance(value, (int, float)):
            value = max(0, int(value))

        sanitized[key] = value

    return sanitized, warnings
