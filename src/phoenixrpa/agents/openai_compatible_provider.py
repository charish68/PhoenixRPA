import asyncio
import json
import urllib.error
import urllib.request

from phoenixrpa.agents.provider import LLMProvider
from phoenixrpa.core.logger import logger


class OpenAICompatibleProvider(LLMProvider):

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        timeout: float = 30.0,
    ):
        if not api_key:
            raise ValueError(
                "LLM API key is required."
            )

        if not model:
            raise ValueError(
                "LLM model is required."
            )

        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def generate(
        self,
        prompt: str,
    ) -> str:

        payload = json.dumps(
            {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            }
        ).encode("utf-8")

        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        def send_request():
            with urllib.request.urlopen(
                request,
                timeout=self.timeout,
            ) as response:
                return json.loads(
                    response.read().decode("utf-8")
                )

        try:
            data = await asyncio.to_thread(
                send_request
            )

            content = (
                data["choices"][0]["message"]["content"]
            )

            if not isinstance(content, str):
                raise ValueError(
                    "LLM response content must be a string."
                )

            return content.strip()

        except (
            urllib.error.URLError,
            TimeoutError,
            KeyError,
            IndexError,
            json.JSONDecodeError,
            ValueError,
        ) as exc:

            logger.error(
                f"LLM provider request failed: {exc}"
            )

            raise RuntimeError(
                f"LLM provider request failed: {exc}"
            ) from exc
