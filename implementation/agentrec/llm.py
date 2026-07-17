"""Provider-agnostic LLM client with a disk cache.

Backends:
- "ollama" (default): local server, no key. Model per config (paper runs: gemma4:e4b).
- "openai": any OpenAI-compatible endpoint. Set AGENTREC_BASE_URL / AGENTREC_API_KEY /
  AGENTREC_MODEL env vars. This is the bring-your-own-key path promised in the paper.

The cache (JSON files under cache/, keyed by SHA256 of backend+model+messages+options)
exists for evaluation-scale throughput: ablation conditions share upstream agent calls,
and re-runs after a crash are free. Delete cache/ to force fresh generation.
"""

import hashlib
import json
import os
import time
import urllib.request
from pathlib import Path


class LLMClient:
    def __init__(self, backend="ollama", model="gemma4:e4b",
                 cache_dir=None, temperature=0.2, num_ctx=8192):
        self.backend = backend
        self.model = os.environ.get("AGENTREC_MODEL", model)
        self.temperature = temperature
        self.num_ctx = num_ctx
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.stats = {"calls": 0, "cache_hits": 0, "total_latency_s": 0.0}

    # ------------------------------------------------------------------ public
    def chat(self, system: str, user: str, force_json: bool = True) -> str:
        key = self._cache_key(system, user, force_json)
        if self.cache_dir:
            hit = self.cache_dir / f"{key}.json"
            if hit.exists():
                self.stats["cache_hits"] += 1
                return json.loads(hit.read_text())["content"]
        t0 = time.time()
        if self.backend == "ollama":
            content = self._ollama(system, user, force_json)
        elif self.backend == "openai":
            content = self._openai_compat(system, user, force_json)
        else:
            raise ValueError(f"unknown backend {self.backend!r}")
        self.stats["calls"] += 1
        self.stats["total_latency_s"] += time.time() - t0
        if self.cache_dir:
            (self.cache_dir / f"{key}.json").write_text(json.dumps(
                {"content": content, "model": self.model, "ts": time.time()}))
        return content

    # ----------------------------------------------------------------- backends
    def _ollama(self, system, user, force_json):
        body = {
            "model": self.model, "stream": False,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "options": {"temperature": self.temperature, "num_ctx": self.num_ctx},
        }
        if force_json:
            body["format"] = "json"
        req = urllib.request.Request(
            os.environ.get("AGENTREC_OLLAMA_URL", "http://localhost:11434") + "/api/chat",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as resp:
            return json.loads(resp.read())["message"]["content"]

    def _openai_compat(self, system, user, force_json):
        base = os.environ["AGENTREC_BASE_URL"].rstrip("/")
        body = {
            "model": self.model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "temperature": self.temperature,
        }
        if force_json:
            body["response_format"] = {"type": "json_object"}
        req = urllib.request.Request(
            base + "/chat/completions",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {os.environ['AGENTREC_API_KEY']}"})
        with urllib.request.urlopen(req, timeout=600) as resp:
            return json.loads(resp.read())["choices"][0]["message"]["content"]

    # ------------------------------------------------------------------- cache
    def _cache_key(self, system, user, force_json):
        blob = json.dumps([self.backend, self.model, self.temperature,
                           system, user, force_json])
        return hashlib.sha256(blob.encode()).hexdigest()[:32]
