from phoenixrpa.agents.provider import LLMProvider


class MockLLMProvider(LLMProvider):

    def __init__(self, response: str):
        self.response = response

    async def generate(
        self,
        prompt: str,
    ) -> str:
        return self.response
