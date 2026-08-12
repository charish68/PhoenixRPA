import json
from unittest.mock import patch

import pytest

from phoenixrpa.agents.openai_compatible_provider import (
    OpenAICompatibleProvider,
)


class FakeResponse:

    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def read(self):
        return json.dumps(
            self.payload
        ).encode("utf-8")


@pytest.mark.asyncio
async def test_openai_compatible_provider_generates_text():

    provider = OpenAICompatibleProvider(
        api_key="test-key",
        model="test-model",
        base_url="https://example.com/v1",
    )

    payload = {
        "choices": [
            {
                "message": {
                    "content": "#emailInputChanged"
                }
            }
        ]
    }

    with patch(
        "phoenixrpa.agents.openai_compatible_provider.urllib.request.urlopen",
        return_value=FakeResponse(payload),
    ) as mock_urlopen:

        result = await provider.generate(
            "Find the replacement selector."
        )

    assert result == "#emailInputChanged"

    request = mock_urlopen.call_args.args[0]

    assert request.full_url == (
        "https://example.com/v1/chat/completions"
    )

    assert request.get_header("Authorization") == (
        "Bearer test-key"
    )


@pytest.mark.asyncio
async def test_openai_compatible_provider_rejects_missing_api_key():

    with pytest.raises(ValueError):
        OpenAICompatibleProvider(
            api_key="",
            model="test-model",
            base_url="https://example.com/v1",
        )


@pytest.mark.asyncio
async def test_openai_compatible_provider_rejects_missing_model():

    with pytest.raises(ValueError):
        OpenAICompatibleProvider(
            api_key="test-key",
            model="",
            base_url="https://example.com/v1",
        )
