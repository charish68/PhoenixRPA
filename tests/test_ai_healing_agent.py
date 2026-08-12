import pytest

from phoenixrpa.agents.healing_agent import AIHealingAgent
from phoenixrpa.agents.mock_provider import MockLLMProvider


@pytest.mark.asyncio
async def test_ai_healing_agent_returns_selector():

    provider = MockLLMProvider(
        "#emailInputChanged"
    )

    agent = AIHealingAgent(provider)

    result = await agent.suggest_selector(
        "#userEmail",
        '<input id="emailInputChanged" type="email">',
    )

    assert result == "#emailInputChanged"


@pytest.mark.asyncio
async def test_ai_healing_agent_returns_none_for_empty_response():

    provider = MockLLMProvider("")

    agent = AIHealingAgent(provider)

    result = await agent.suggest_selector(
        "#userEmail",
        "<input>",
    )

    assert result is None
