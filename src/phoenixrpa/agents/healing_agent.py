from phoenixrpa.agents.base import HealingAgent
from phoenixrpa.agents.provider import LLMProvider


class AIHealingAgent(HealingAgent):

    def __init__(
        self,
        provider: LLMProvider,
    ):
        self.provider = provider

    async def suggest_selector(
        self,
        failed_selector: str,
        page_context: str,
    ) -> str | None:

        prompt = f"""
You are a browser automation selector healing agent.

A Playwright selector failed:

{failed_selector}

The current page context is:

{page_context}

Return ONLY the best replacement CSS selector.
Do not explain your answer.
"""

        response = await self.provider.generate(prompt)

        selector = response.strip()

        if not selector:
            return None

        return selector
