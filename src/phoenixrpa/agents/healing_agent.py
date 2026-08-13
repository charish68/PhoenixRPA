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

Rules:
1. Return a selector that matches an element explicitly present in the page context.
2. Do not invent IDs, classes, attributes, or elements.
3. If an element has an id, prefer the exact CSS id selector using that id.
4. The replacement must be a valid CSS selector.
5. Return ONLY the selector.
6. Do not explain your answer.
"""

        response = await self.provider.generate(prompt)

        selector = response.strip()

        if not selector:
            return None

        return selector
