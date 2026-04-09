#!/usr/bin/env python3
"""
AI image generation module for 爆款智坊.

Supports multiple providers via a simple abstraction:
  - doubao-seedream (Volcengine Ark) — default, good for Chinese prompts
  - openai (DALL-E 3) — broad availability
  - gemini (Google Gemini Imagen) — multimodal image generation
  - dashscope (Alibaba Tongyi Wanxiang) — good for Chinese prompts
  - minimax — Chinese provider
  - replicate — open-source models
  - azure_openai — Azure-hosted DALL-E
  - openrouter — multi-model proxy
  - jimeng (ByteDance) — good for Chinese prompts
  - Custom providers via ImageProvider base class

Usage as CLI:
    python3 image_gen.py --prompt "描述" --output cover.png
    python3 image_gen.py --prompt "描述" --output cover.png --size cover
    python3 image_gen.py --prompt "描述" --output cover.png --provider gemini

Usage as module:
    from image_gen import generate_image
    path = generate_image("prompt text", "output.png", size="cover")
"""

import abc
import argparse
import base64
import hashlib
import hmac
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

# --- Config ---

CONFIG_PATHS = [
    Path.cwd() / "config.yaml",
    Path(__file__).parent.parent / "config.yaml",  # skill root
    Path(__file__).parent / "config.yaml",          # toolkit dir
    Path.home() / ".config" / "wewrite" / "config.yaml",
]


def _load_config() -> dict:
    for p in CONFIG_PATHS:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
    return {}


# --- Size presets ---

# Cover: 2.35:1 微信封面比例
# Article: 16:9 横版内文配图
# Vertical: 9:16 竖版
_DEFAULT = "1792x1024"
_DEFAULT_V = "1024x1792"
_DEFAULT_SQ = "1024x1024"

SIZE_PRESETS = {
    "cover": {
        "doubao": "2952x1256", "openai": _DEFAULT, "gemini": _DEFAULT,
        "dashscope": _DEFAULT, "minimax": _DEFAULT, "replicate": _DEFAULT,
        "azure_openai": _DEFAULT, "openrouter": _DEFAULT, "jimeng": _DEFAULT,
    },
    "article": {
        "doubao": "2560x1440", "openai": _DEFAULT, "gemini": _DEFAULT,
        "dashscope": _DEFAULT, "minimax": _DEFAULT, "replicate": _DEFAULT,
        "azure_openai": _DEFAULT, "openrouter": _DEFAULT, "jimeng": _DEFAULT,
    },
    "vertical": {
        "doubao": "1088x2560", "openai": _DEFAULT_V, "gemini": _DEFAULT_V,
        "dashscope": _DEFAULT_V, "minimax": _DEFAULT_V, "replicate": _DEFAULT_V,
        "azure_openai": _DEFAULT_V, "openrouter": _DEFAULT_V, "jimeng": _DEFAULT_V,
    },
    "square": {
        "doubao": "2048x2048", "openai": _DEFAULT_SQ, "gemini": _DEFAULT_SQ,
        "dashscope": _DEFAULT_SQ, "minimax": _DEFAULT_SQ, "replicate": _DEFAULT_SQ,
        "azure_openai": _DEFAULT_SQ, "openrouter": _DEFAULT_SQ, "jimeng": _DEFAULT_SQ,
    },
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def _compress_image(raw_bytes: bytes, max_size: int) -> bytes:
    """Compress image to fit under max_size by reducing JPEG quality."""
    from io import BytesIO
    from PIL import Image

    img = Image.open(BytesIO(raw_bytes))
    if img.mode == "RGBA":
        img = img.convert("RGB")

    for quality in (90, 80, 70, 60, 50):
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        if buf.tell() <= max_size:
            return buf.getvalue()

    return buf.getvalue()


def _size_to_aspect(size: str) -> str:
    """Convert 'WxH' to nearest standard aspect ratio string."""
    if ":" in size:
        return size
    try:
        w, h = (int(x) for x in size.split("x", 1))
    except ValueError:
        return "16:9"
    ratio = w / h
    for ar, val in [("1:1", 1.0), ("16:9", 16/9), ("9:16", 9/16),
                    ("4:3", 4/3), ("3:4", 3/4), ("3:2", 3/2), ("2:3", 2/3)]:
        if abs(ratio - val) < 0.15:
            return ar
    return "16:9"


def _download_image(url: str) -> bytes:
    """Download image bytes from URL."""
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.content


# --- Provider abstraction ---

class ImageProvider(abc.ABC):
    """Base class for image generation providers."""

    @abc.abstractmethod
    def generate(self, prompt: str, size: str) -> bytes:
        """Generate an image and return raw bytes."""
        ...

    def resolve_size(self, preset: str) -> str:
        """Resolve a size preset to a concrete size string for this provider."""
        provider_key = self.provider_key
        if preset in SIZE_PRESETS:
            return SIZE_PRESETS[preset].get(provider_key, list(SIZE_PRESETS[preset].values())[0])
        return preset

    @property
    @abc.abstractmethod
    def provider_key(self) -> str:
        ...


# --- Providers ---

class DoubaoProvider(ImageProvider):
    """doubao-seedream via Volcengine Ark API."""

    provider_key = "doubao"

    def __init__(self, api_key: str, model: str = "doubao-seedream-5-0-260128",
                 base_url: str = "https://ark.cn-beijing.volces.com/api/v3", **_kw):
        self._api_key = api_key
        self._model = model
        self._base_url = base_url

    def generate(self, prompt: str, size: str) -> bytes:
        resp = requests.post(
            f"{self._base_url}/images/generations",
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self._api_key}"},
            json={"model": self._model, "prompt": prompt,
                  "response_format": "url", "size": size,
                  "stream": False, "watermark": False},
            timeout=120,
        )
        data = resp.json()
        if resp.status_code != 200:
            raise ValueError(f"Doubao error ({resp.status_code}): "
                             f"{data.get('error', {}).get('message', str(data))}")
        url = data.get("data", [{}])[0].get("url")
        if not url:
            raise ValueError(f"No image URL: {data}")
        return _download_image(url)


class OpenAIProvider(ImageProvider):
    """OpenAI DALL-E 3 provider."""

    provider_key = "openai"

    def __init__(self, api_key: str, model: str = "dall-e-3",
                 base_url: str = "https://api.openai.com/v1", **_kw):
        self._api_key = api_key
        self._model = model
        self._base_url = base_url

    def generate(self, prompt: str, size: str) -> bytes:
        resp = requests.post(
            f"{self._base_url}/images/generations",
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self._api_key}"},
            json={"model": self._model, "prompt": prompt,
                  "n": 1, "size": size, "response_format": "url"},
            timeout=120,
        )
        data = resp.json()
        if resp.status_code != 200:
            raise ValueError(f"OpenAI error ({resp.status_code}): "
                             f"{data.get('error', {}).get('message', str(data))}")
        url = data.get("data", [{}])[0].get("url")
        if not url:
            raise ValueError(f"No image URL: {data}")
        return _download_image(url)


class GeminiProvider(ImageProvider):
    """Google Gemini Imagen provider."""

    provider_key = "gemini"

    def __init__(self, api_key: str, model: str = "gemini-3.1-flash-image-preview",
                 base_url: str = "https://generativelanguage.googleapis.com/v1beta", **_kw):
        self._api_key = api_key
        self._model = model
        self._base_url = base_url

    def generate(self, prompt: str, size: str) -> bytes:
        if "x" in size:
            w, h = size.split("x", 1)
            prompt = f"{prompt}\n\nGenerate this image at {w}x{h} resolution."
        resp = requests.post(
            f"{self._base_url}/models/{self._model}:generateContent",
            headers={"Content-Type": "application/json",
                     "x-goog-api-key": self._api_key},
            json={"contents": [{"parts": [{"text": prompt}]}],
                  "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}},
            timeout=120,
        )
        if resp.status_code != 200:
            msg = resp.text[:200]
            try:
                msg = resp.json().get("error", {}).get("message", msg)
            except Exception:
                pass
            raise ValueError(f"Gemini error ({resp.status_code}): {msg}")
        for part in resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", []):
            inline = part.get("inlineData")
            if inline and inline.get("mimeType", "").startswith("image/"):
                return base64.b64decode(inline["data"])
        raise ValueError("No image in Gemini response")


class DashScopeProvider(ImageProvider):
    """Alibaba Tongyi Wanxiang (通义万相) via DashScope API."""

    provider_key = "dashscope"

    def __init__(self, api_key: str, model: str = "qwen-image-2.0-pro",
                 base_url: str = "https://dashscope.aliyuncs.com/api/v1", **_kw):
        self._api_key = api_key
        self._model = model
        self._base_url = base_url

    def generate(self, prompt: str, size: str) -> bytes:
        ds_size = size.replace("x", "*")  # DashScope uses "W*H"
        resp = requests.post(
            f"{self._base_url}/services/aigc/multimodal-generation/generation",
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self._api_key}"},
            json={
                "model": self._model,
                "input": {"messages": [{"role": "user", "content": [{"text": prompt}]}]},
                "parameters": {"prompt_extend": False, "size": ds_size, "watermark": False},
            },
            timeout=120,
        )
        data = resp.json()
        if resp.status_code != 200:
            raise ValueError(f"DashScope error ({resp.status_code}): "
                             f"{data.get('message', str(data))}")
        # Try output.result_image first, then output.choices
        output = data.get("output", {})
        img = output.get("result_image")
        if not img:
            choices = output.get("choices", [])
            if choices:
                for c in choices[0].get("message", {}).get("content", []):
                    if "image" in c:
                        img = c["image"]
                        break
        if not img:
            raise ValueError(f"No image in DashScope response: {data}")
        if img.startswith("http"):
            return _download_image(img)
        return base64.b64decode(img)


class MiniMaxProvider(ImageProvider):
    """MiniMax image generation."""

    provider_key = "minimax"

    def __init__(self, api_key: str, model: str = "image-01",
                 base_url: str = "https://api.minimax.io/v1", **_kw):
        self._api_key = api_key
        self._model = model
        self._base_url = base_url

    def generate(self, prompt: str, size: str) -> bytes:
        w, h = 1024, 1024
        try:
            w, h = (int(x) for x in size.split("x", 1))
        except ValueError:
            pass
        resp = requests.post(
            f"{self._base_url}/image_generation",
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self._api_key}"},
            json={"model": self._model, "prompt": prompt,
                  "response_format": "base64",
                  "width": w, "height": h, "n": 1},
            timeout=120,
        )
        data = resp.json()
        if resp.status_code != 200:
            raise ValueError(f"MiniMax error ({resp.status_code}): {data}")
        b64_list = data.get("data", {}).get("image_base64", [])
        if not b64_list:
            raise ValueError(f"No image in MiniMax response: {data}")
        return base64.b64decode(b64_list[0])


class ReplicateProvider(ImageProvider):
    """Replicate API — supports many open-source image models."""

    provider_key = "replicate"
    _POLL_INTERVAL = 2
    _POLL_TIMEOUT = 300

    def __init__(self, api_key: str, model: str = "google/nano-banana-pro",
                 base_url: str = "https://api.replicate.com/v1", **_kw):
        self._api_key = api_key
        self._model = model
        self._base_url = base_url

    def generate(self, prompt: str, size: str) -> bytes:
        aspect = _size_to_aspect(size)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {self._api_key}",
                   "Prefer": "wait=60"}
        resp = requests.post(
            f"{self._base_url}/models/{self._model}/predictions",
            headers=headers,
            json={"input": {"prompt": prompt, "aspect_ratio": aspect,
                            "number_of_images": 1, "output_format": "png"}},
            timeout=120,
        )
        data = resp.json()
        if resp.status_code not in (200, 201):
            raise ValueError(f"Replicate error ({resp.status_code}): {data}")

        # Poll if not completed yet
        poll_url = data.get("urls", {}).get("get")
        deadline = time.monotonic() + self._POLL_TIMEOUT
        while data.get("status") not in ("succeeded", "failed", "canceled"):
            if time.monotonic() > deadline:
                raise ValueError("Replicate polling timeout")
            time.sleep(self._POLL_INTERVAL)
            data = requests.get(poll_url, headers=headers, timeout=30).json()

        if data.get("status") != "succeeded":
            raise ValueError(f"Replicate failed: {data.get('error')}")

        output = data.get("output")
        if isinstance(output, list):
            output = output[0]
        if isinstance(output, dict):
            output = output.get("url", output.get("uri"))
        if not output or not isinstance(output, str):
            raise ValueError(f"No image URL in Replicate output: {data}")
        return _download_image(output)


class AzureOpenAIProvider(ImageProvider):
    """Azure-hosted OpenAI DALL-E."""

    provider_key = "azure_openai"

    def __init__(self, api_key: str, model: str = "dall-e-3",
                 base_url: str = "", deployment: str = "", **_kw):
        self._api_key = api_key
        self._deployment = deployment or model
        self._base_url = base_url.rstrip("/")

    def generate(self, prompt: str, size: str) -> bytes:
        if not self._base_url:
            raise ValueError("Azure OpenAI requires base_url "
                             "(e.g. https://YOUR-RESOURCE.openai.azure.com/openai)")
        resp = requests.post(
            f"{self._base_url}/deployments/{self._deployment}"
            f"/images/generations?api-version=2025-04-01-preview",
            headers={"Content-Type": "application/json",
                     "api-key": self._api_key},
            json={"prompt": prompt, "size": size, "n": 1, "quality": "medium"},
            timeout=120,
        )
        data = resp.json()
        if resp.status_code != 200:
            raise ValueError(f"Azure OpenAI error ({resp.status_code}): {data}")
        item = data.get("data", [{}])[0]
        if item.get("url"):
            return _download_image(item["url"])
        if item.get("b64_json"):
            return base64.b64decode(item["b64_json"])
        raise ValueError(f"No image in Azure response: {data}")


class OpenRouterProvider(ImageProvider):
    """OpenRouter — multi-model proxy using chat completions format."""

    provider_key = "openrouter"

    def __init__(self, api_key: str, model: str = "google/gemini-3.1-flash-image-preview",
                 base_url: str = "https://openrouter.ai/api/v1", **_kw):
        self._api_key = api_key
        self._model = model
        self._base_url = base_url

    def generate(self, prompt: str, size: str) -> bytes:
        aspect = _size_to_aspect(size)
        resp = requests.post(
            f"{self._base_url}/chat/completions",
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self._api_key}"},
            json={
                "model": self._model,
                "messages": [{"role": "user", "content": prompt}],
                "modalities": ["image"],
                "stream": False,
                "image_config": {"aspect_ratio": aspect},
                "provider": {"require_parameters": True},
            },
            timeout=120,
        )
        data = resp.json()
        if resp.status_code != 200:
            raise ValueError(f"OpenRouter error ({resp.status_code}): {data}")

        # Extract image from multiple possible locations
        choice = data.get("choices", [{}])[0].get("message", {})
        # Path 1: images array
        images = choice.get("images", [])
        if images:
            img = images[0]
            if img.startswith("http"):
                return _download_image(img)
            if img.startswith("data:"):
                _, b64 = img.split(",", 1)
                return base64.b64decode(b64)
        # Path 2: content array with image items
        content = choice.get("content", [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "image":
                    url = item.get("url") or item.get("image_url", {}).get("url")
                    if url:
                        if url.startswith("data:"):
                            _, b64 = url.split(",", 1)
                            return base64.b64decode(b64)
                        return _download_image(url)
        raise ValueError(f"No image in OpenRouter response: {data}")


class JimengProvider(ImageProvider):
    """ByteDance Jimeng (即梦) — async submit + poll with HMAC-SHA256 auth."""

    provider_key = "jimeng"
    _POLL_INTERVAL = 2
    _POLL_MAX_ATTEMPTS = 60

    def __init__(self, api_key: str, secret_key: str = "",
                 model: str = "jimeng_t2i_v40",
                 base_url: str = "https://visual.volcengineapi.com", **_kw):
        self._access_key = api_key
        self._secret_key = secret_key
        self._model = model
        self._base_url = base_url

    def _sign(self, method: str, path: str, query: str,
              headers: dict, payload: bytes) -> dict:
        """Generate Volcengine HMAC-SHA256 signed headers."""
        now = datetime.now(timezone.utc)
        date_stamp = now.strftime("%Y%m%d")
        amz_date = now.strftime("%Y%m%dT%H%M%SZ")

        signed_headers_list = sorted(k.lower() for k in headers)
        signed_headers_str = ";".join(signed_headers_list)

        canonical = "\n".join([
            method, path, query,
            "".join(f"{k.lower()}:{headers[k]}\n" for k in sorted(headers)),
            signed_headers_str,
            hashlib.sha256(payload).hexdigest(),
        ])

        region = "cn-north-1"
        service = "cv"
        scope = f"{date_stamp}/{region}/{service}/request"
        string_to_sign = "\n".join([
            "HMAC-SHA256", amz_date, scope,
            hashlib.sha256(canonical.encode()).hexdigest(),
        ])

        def _hmac(key: bytes, msg: str) -> bytes:
            return hmac.new(key, msg.encode(), hashlib.sha256).digest()

        k_date = _hmac(self._secret_key.encode(), date_stamp)
        k_region = _hmac(k_date, region)
        k_service = _hmac(k_region, service)
        k_signing = _hmac(k_service, "request")
        signature = hmac.new(k_signing, string_to_sign.encode(),
                             hashlib.sha256).hexdigest()

        auth = (f"HMAC-SHA256 Credential={self._access_key}/{scope}, "
                f"SignedHeaders={signed_headers_str}, Signature={signature}")
        return {**headers, "Authorization": auth, "X-Date": amz_date}

    def _request(self, action: str, body: dict) -> dict:
        payload = json.dumps(body).encode()
        path = "/"
        query = f"Action={action}&Version=2022-08-31"
        headers = {
            "Content-Type": "application/json",
            "Host": self._base_url.replace("https://", "").replace("http://", ""),
        }
        signed = self._sign("POST", path, query, headers, payload)
        resp = requests.post(
            f"{self._base_url}/?{query}",
            headers=signed, data=payload, timeout=120,
        )
        data = resp.json()
        if resp.status_code != 200:
            raise ValueError(f"Jimeng error ({resp.status_code}): {data}")
        return data

    def generate(self, prompt: str, size: str) -> bytes:
        if not self._secret_key:
            raise ValueError("Jimeng requires both api_key (access_key_id) "
                             "and secret_key (secret_access_key)")
        w, h = 1024, 1024
        try:
            w, h = (int(x) for x in size.split("x", 1))
        except ValueError:
            pass

        # Submit task
        submit = self._request("CVSync2AsyncSubmitTask", {
            "req_key": self._model, "prompt": prompt,
            "width": w, "height": h,
        })
        task_id = submit.get("data", {}).get("task_id")
        if not task_id:
            raise ValueError(f"No task_id from Jimeng: {submit}")

        # Poll for result
        for _ in range(self._POLL_MAX_ATTEMPTS):
            time.sleep(self._POLL_INTERVAL)
            result = self._request("CVSync2AsyncGetResult", {
                "req_key": self._model, "task_id": task_id,
            })
            code = result.get("code")
            if code == 10000:
                data = result.get("data", {})
                b64_list = data.get("binary_data_base64", [])
                if b64_list:
                    return base64.b64decode(b64_list[0])
                urls = data.get("image_urls", [])
                if urls:
                    return _download_image(urls[0])
                raise ValueError(f"No image data in Jimeng result: {result}")
            if code and code != 10000:
                status = result.get("data", {}).get("status")
                if status in ("failed", "canceled"):
                    raise ValueError(f"Jimeng task failed: {result}")

        raise ValueError("Jimeng polling timeout")


# --- Provider registry ---

PROVIDERS = {
    "doubao": DoubaoProvider,
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
    "dashscope": DashScopeProvider,
    "minimax": MiniMaxProvider,
    "replicate": ReplicateProvider,
    "azure_openai": AzureOpenAIProvider,
    "openrouter": OpenRouterProvider,
    "jimeng": JimengProvider,
}


def _build_provider_from_entry(entry: dict) -> ImageProvider:
    """Build a single ImageProvider from a provider config entry."""
    provider_name = entry.get("provider", "doubao")
    api_key = entry.get("api_key")

    if not api_key:
        raise ValueError(f"No api_key for provider '{provider_name}'")

    provider_cls = PROVIDERS.get(provider_name)
    if not provider_cls:
        raise ValueError(
            f"Unknown provider: '{provider_name}'. "
            f"Available: {', '.join(PROVIDERS.keys())}"
        )

    kwargs = {"api_key": api_key}
    if entry.get("model"):
        kwargs["model"] = entry["model"]
    if entry.get("base_url"):
        kwargs["base_url"] = entry["base_url"]
    if entry.get("secret_key"):
        kwargs["secret_key"] = entry["secret_key"]
    if entry.get("deployment"):
        kwargs["deployment"] = entry["deployment"]

    return provider_cls(**kwargs)


def _build_provider_chain(config: dict) -> list[ImageProvider]:
    """Build an ordered list of providers to try.

    Supports two config formats:
      - Legacy:  image.provider + image.api_key (single provider)
      - New:     image.providers (list, tried in order with auto-fallback)
    """
    img_cfg = config.get("image", {})
    providers_list = img_cfg.get("providers")

    if providers_list and isinstance(providers_list, list):
        chain = []
        for entry in providers_list:
            try:
                chain.append(_build_provider_from_entry(entry))
            except ValueError:
                continue  # skip misconfigured entries
        if not chain:
            raise ValueError(
                "No valid providers in image.providers list. "
                "Each entry needs 'provider' and 'api_key'."
            )
        return chain

    # Legacy single-provider format
    api_key = img_cfg.get("api_key")
    if not api_key:
        raise ValueError(
            "image.api_key not set in config.yaml. "
            "Configure your API key to enable image generation."
        )
    return [_build_provider_from_entry(img_cfg)]


def _build_provider(config: dict) -> ImageProvider:
    """Build an ImageProvider from config.yaml (backward-compatible entry point)."""
    return _build_provider_chain(config)[0]


# --- Public API ---

def generate_image(
    prompt: str,
    output_path: str,
    size: str = "cover",
    config: dict = None,
) -> str:
    """
    Generate an image using configured providers with auto-fallback.

    Tries each provider in order. If one fails, falls back to the next.
    Supports both single-provider (legacy) and multi-provider config.

    Args:
        prompt: Image generation prompt (Chinese or English).
        output_path: Where to save the image.
        size: Size preset ("cover", "article", "vertical", "square") or explicit "WxH".
        config: Optional config dict. If None, loads from config.yaml.

    Returns:
        The output file path.
    """
    if config is None:
        config = _load_config()

    chain = _build_provider_chain(config)
    last_error = None

    for provider in chain:
        resolved_size = provider.resolve_size(size)
        try:
            raw_bytes = provider.generate(prompt, resolved_size)
        except Exception as e:
            last_error = e
            print(
                f"Provider '{provider.provider_key}' failed: {e}. "
                f"Trying next...",
                file=sys.stderr,
            )
            continue

        # Compress if over 5MB (WeChat upload limit)
        if len(raw_bytes) > MAX_FILE_SIZE:
            raw_bytes = _compress_image(raw_bytes, MAX_FILE_SIZE)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(raw_bytes)
        return str(output)

    raise ValueError(
        f"All providers failed. Last error: {last_error}"
    )


def main():
    ap = argparse.ArgumentParser(description="Generate images using AI")
    ap.add_argument("--prompt", required=True, help="Image generation prompt")
    ap.add_argument("--output", required=True, help="Output file path")
    ap.add_argument("--size", default="cover",
                    help="Size: cover, article, vertical, square, or WxH")
    ap.add_argument("--provider", default=None,
                    help=f"Override provider ({', '.join(PROVIDERS)})")
    args = ap.parse_args()

    try:
        config = _load_config()
        if args.provider:
            config.setdefault("image", {})["provider"] = args.provider
        path = generate_image(args.prompt, args.output, size=args.size, config=config)
        print(f"Image saved: {path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


# ─── Poster / 小绿书卡片渲染 ───────────────────────────────────────────────

import re
import subprocess
from io import BytesIO

# Tone perception palette (shared with ljg-card -m mode)
TONE_MAP = [
    (("认知", "思维", "本质", "意义", "哲学"), "#FAF8F4", "#7C6853"),
    (("架构", "模型", "算法", "系统", "代码", "技术", "工程"), "#F5F7FA", "#3D5A80"),
    (("故事", "人物", "写作", "文字", "诗", "文学", "叙事"), "#FBF9F1", "#6B4E3D"),
    (("实验", "数据", "发现", "论文", "研究", "科学"), "#F4F8F6", "#2D6A4F"),
]
DEFAULT_TONE = ("#FAFAF8", "#4A4A4A")


def _detect_tone(text: str) -> tuple[str, str]:
    """Detect content tone and return (bg_color, accent_color)."""
    for keywords, bg, accent in TONE_MAP:
        if any(kw in text for kw in keywords):
            return bg, accent
    return DEFAULT_TONE


def _parse_markdown_elements(text: str) -> list[tuple[str, str]]:
    """Parse markdown text into elements with types.

    Returns list of (element_type, content) where types are:
    h1, h2, h3, p, blockquote, bold, list, divider, gold, empty
    """
    lines = text.splitlines()
    elements = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Heading
        if line.startswith("# "):
            elements.append(("h1", line[2:].strip()))
        elif line.startswith("## "):
            elements.append(("h2", line[3:].strip()))
        elif line.startswith("### "):
            elements.append(("h3", line[4:].strip()))
        # Blockquote
        elif line.startswith(">"):
            elements.append(("blockquote", line[1:].strip()))
        # List
        elif line.startswith("- ") or line.startswith("* "):
            elements.append(("list", line[2:].strip()))
        # Divider
        elif line.startswith("---") or line.startswith("***"):
            elements.append(("divider", ""))
        # Empty
        elif not line:
            elements.append(("empty", ""))
        # Gold sentence detection: short standalone line (<25 chars, not starting with emoji)
        elif len(line) < 25 and i > 0 and lines[i-1].strip() == "":
            elements.append(("gold", line))
        # Paragraph
        else:
            # Process inline bold
            clean = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
            elements.append(("p", clean))
        i += 1
    return elements


# Visual weight constants (from mode-poster.md step 3)
WEIGHT = {
    "p": 1.4,
    "h1": 6.0,
    "h2": 3.5,
    "h3": 2.5,
    "gold": 3.0,
    "item": 1.8,
    "blockquote": 1.7,
    "divider": 60,
    "list": 1.4,
    "empty": 0,
}
CARD_THRESHOLD = 380  # per card


def _estimate_weight(elem_type: str, content: str) -> float:
    """Estimate visual weight of an element."""
    base = WEIGHT.get(elem_type, 1.4)
    if elem_type in ("empty", "divider"):
        return base
    return len(content) * base


def _greedy_split(elements: list[tuple[str, str]]) -> list[list[tuple[str, str]]]:
    """Greedy split elements into cards of ~380 weight each.

    Hard rules:
    - Never leave h1 alone on a card (must travel with at least one content element)
    - Never cut mid-sentence; prefer paragraph/divider boundaries
    """
    cards = []
    current_card = []
    current_weight = 0.0

    i = 0
    while i < len(elements):
        elem_type, content = elements[i]
        w = _estimate_weight(elem_type, content)

        # Hard rule: h1 must travel with at least one non-empty element.
        # If current card is non-empty and we're about to put h1 alone on a new card,
        # commit current card and carry h1 into the next iteration.
        if elem_type == "h1" and current_weight > 0:
            # Finalize current card before starting h1 card
            if current_card:
                cards.append(current_card)
            current_card = []
            current_weight = 0.0
            # Fall through: h1 will be evaluated in next iteration with weight=0

        elif current_weight + w > CARD_THRESHOLD and current_weight > 0:
            # Threshold exceeded: commit current card
            # Exception: if current card is near-empty AND this is p/blockquote/list,
            # let it overflow rather than start a near-empty card
            if elem_type in ("p", "blockquote", "list") and current_weight < CARD_THRESHOLD * 0.5:
                current_card.append((elem_type, content))
                current_weight += w
            else:
                cards.append(current_card)
                current_card = [(elem_type, content)]
                current_weight = w
        else:
            current_card.append((elem_type, content))
            current_weight += w
        i += 1

    if current_card:
        cards.append(current_card)

    return cards if cards else [[]]


def _elements_to_html(elements: list[tuple[str, str]], is_last: bool) -> str:
    """Convert parsed elements to HTML body fragment."""
    html_parts = []
    i = 0
    while i < len(elements):
        elem_type, content = elements[i]
        if elem_type == "empty":
            pass  # spacing handled by margins
        elif elem_type == "h1":
            html_parts.append(f"<h2>{content}</h2>")
        elif elem_type == "h2":
            html_parts.append(f"<h2>{content}</h2>")
        elif elem_type == "h3":
            html_parts.append(f"<h2 style='font-size:36px'>{content}</h2>")
        elif elem_type == "p":
            html_parts.append(f"<p>{content}</p>")
        elif elem_type == "gold":
            html_parts.append(f"<p class='highlight'>{content}</p>")
        elif elem_type == "blockquote":
            html_parts.append(f"<blockquote><p>{content}</p></blockquote>")
        elif elem_type == "list":
            html_parts.append(f"<ul><li>{content}</li></ul>")
        elif elem_type == "divider":
            html_parts.append("<div class='divider'></div>")
        i += 1

    body = "".join(html_parts)
    if is_last:
        body += "<p style='text-align:right;font-size:16px;color:#ACACB0;margin-top:40px;'>∎</p>"
    return body


def _render_card_html(
    card_elements: list[tuple[str, str]],
    template_path: Path,
    bg_color: str,
    accent_color: str,
    card_index: int,
    total_cards: int,
    article_title: str = "",
    logo_path: str = "",
    source: str = "",
    author_name: str = "",
) -> str:
    """Render a single card to HTML string."""
    template = template_path.read_text(encoding="utf-8")

    is_last = card_index == total_cards - 1
    is_single = total_cards == 1
    is_continuation = card_index > 0

    # HEADER_BLOCK
    if is_continuation and article_title:
        header_block = f"<div class='header'><span class='running-title'>{article_title}</span></div>"
    else:
        header_block = ""

    # TITLE_BLOCK — extract first h1 from card_elements
    title_block = ""
    for et, ec in card_elements:
        if et == "h1":
            title_block = f"<div class='title-area'><h1>{ec}</h1></div>"
            break

    # BODY_HTML
    body_html = _elements_to_html(card_elements, is_last)

    # PAGE_INFO
    page_info = "" if is_single else f"{card_index + 1} / {total_cards}"

    # SOURCE_LINE (footer)
    source_line = f"<span class='info-source'>{source}</span>" if source else ""

    # Logo path
    logo = str(logo_path) if logo_path else ""

    rendered = (
        template
        .replace("{{BG_COLOR}}", bg_color)
        .replace("{{ACCENT_COLOR}}", accent_color)
        .replace("{{HEADER_BLOCK}}", header_block)
        .replace("{{TITLE_BLOCK}}", title_block)
        .replace("{{BODY_HTML}}", body_html)
        .replace("{{PAGE_INFO}}", page_info)
        .replace("{{SOURCE_LINE}}", source_line)
        .replace("{{LOGO_PATH}}", logo)
        .replace("{{AUTHOR_NAME}}", author_name)
    )
    return rendered


def _capture_screenshot(
    html_path: str,
    output_path: str,
    capture_script: Path,
    width: int = 1080,
    height: int = 1440,
) -> str:
    """Run capture.js to screenshot an HTML file, return PNG path."""
    cmd = [
        "node",
        str(capture_script),
        html_path,
        output_path,
        str(width),
        str(height),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"capture.js failed: {result.stderr.strip()}")
    return result.stdout.strip().replace("OK: ", "")


def render_poster(
    content: str,
    output_dir: str = "/tmp",
    article_title: str = "",
    source: str = "",
    name: str = "poster",
    author_name: str = "爆款智坊",
) -> list[str]:
    """
    Render a 小绿书 (XHS poster cards) from markdown content.

    Pipeline: tone perception → parse → greedy split → HTML render → screenshot

    Args:
        content: Markdown text (may contain headings, paragraphs, bold, lists, blockquotes)
        output_dir: Directory to write PNG files
        article_title: Running title for continuation cards
        source: Source attribution for footer
        name: Base name for output files

    Returns:
        List of PNG file paths (one per card)
    """
    import tempfile

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Resolve asset paths relative to this file
    toolkit_dir = Path(__file__).parent
    assets_dir = toolkit_dir / "assets"
    template_path = assets_dir / "poster_template.html"
    capture_script = assets_dir / "capture.js"
    logo_path = assets_dir / "logo.png"

    if not template_path.exists():
        raise FileNotFoundError(f"poster_template.html not found at {template_path}")
    if not capture_script.exists():
        raise FileNotFoundError(f"capture.js not found at {capture_script}")

    # 1. Tone perception
    bg_color, accent_color = _detect_tone(content)

    # 2. Parse markdown into elements
    elements = _parse_markdown_elements(content)

    # 3. Greedy split into cards
    cards = _greedy_split(elements)
    if not cards or not cards[0]:
        raise ValueError("Content produced no cards")

    total = len(cards)

    # 4. Render each card and screenshot
    png_paths = []
    tmp_htmls = []

    for idx, card_elems in enumerate(cards):
        card_html = _render_card_html(
            card_elements=card_elems,
            template_path=template_path,
            bg_color=bg_color,
            accent_color=accent_color,
            card_index=idx,
            total_cards=total,
            article_title=article_title,
            logo_path=str(logo_path),
            source=source,
            author_name=author_name,
        )
        # Write temp HTML
        tmp_html = Path(tempfile.gettempdir()) / f"ljg_poster_{name}_{idx+1}.html"
        tmp_html.write_text(card_html, encoding="utf-8")
        tmp_htmls.append(tmp_html)

        # Screenshot
        png_file = output_path / f"{name}_{idx+1}.png"
        _capture_screenshot(str(tmp_html), str(png_file), capture_script)
        png_paths.append(str(png_file))

    # Cleanup temp HTMLs
    for hp in tmp_htmls:
        try:
            hp.unlink()
        except Exception:
            pass

    return png_paths
