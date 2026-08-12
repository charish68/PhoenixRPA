from abc import ABC, abstractmethod


class HealingAgent(ABC):

    @abstractmethod
    async def suggest_selector(
        self,
        failed_selector: str,
        page_context: str,
    ) -> str | None:
        """
        Suggest a replacement selector for a failed selector.
        """
        raise NotImplementedError
