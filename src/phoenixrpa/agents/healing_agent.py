import re

from phoenixrpa.agents.base import HealingAgent
from phoenixrpa.agents.provider import LLMProvider


class AIHealingAgent(HealingAgent):

    def __init__(
        self,
        provider: LLMProvider,
    ):
        self.provider = provider

    @staticmethod
    def _extract_selector(response: str) -> str | None:
        """
        Extract a selector from an LLM response.

        The model is instructed to return only a selector, but
        production LLM responses may occasionally include markdown
        or explanatory text.
        """

        if not response:
            return None

        text = response.strip()

        if not text:
            return None

        # Remove markdown code fences.
        text = (
            text
            .replace("```css", "")
            .replace("```CSS", "")
            .replace("```", "")
            .strip()
        )

        # Prefer a CSS ID selector when one appears in the response.

        id_match = re.search(
            r"#[A-Za-z_][A-Za-z0-9_-]*",
            text,
        )

        if id_match:
            return id_match.group(0)

        # Look for a common CSS selector beginning with an HTML element.
        selector_match = re.search(
            r"\b(?:input|textarea|button|a|select)"
            r"(?:#[A-Za-z_][A-Za-z0-9_-]*)?"
            r"(?:\.[A-Za-z_][A-Za-z0-9_-]*)?",
            text,
            re.IGNORECASE,
        )

        if selector_match:
            return selector_match.group(0)

        # Fall back to the original response. Playwright validation
        # remains the final safety check.
        return text

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

        return self._extract_selector(response)


