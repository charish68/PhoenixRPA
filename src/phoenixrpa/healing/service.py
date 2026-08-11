from difflib import SequenceMatcher

from playwright.async_api import Page

from phoenixrpa.core.logger import logger


class HealingService:

    def __init__(self, page: Page):
        self.page = page

    async def find_best_selector(
        self,
        failed_selector: str,
    ) -> str | None:

        logger.info(
            f"Attempting selector healing for: {failed_selector}"
        )

        # --------------------------------------------------------
        # 1. Check whether original selector still exists
        # --------------------------------------------------------

        try:
            locator = self.page.locator(failed_selector)

            if await locator.count() > 0:
                logger.info(
                    f"Original selector still exists: {failed_selector}"
                )
                return failed_selector

        except Exception:
            pass

        # --------------------------------------------------------
        # 2. Extract selector hint
        # --------------------------------------------------------

        failed_hint = (
            failed_selector
            .replace("#", "")
            .replace(".", "")
            .replace("[", "")
            .replace("]", "")
            .replace('"', "")
            .replace("'", "")
            .lower()
        )

        # --------------------------------------------------------
        # 3. Find possible elements
        # --------------------------------------------------------

        candidates = await self.page.locator(
            "input, textarea, button, a, select"
        ).all()

        best_selector = None
        best_score = 0

        for element in candidates:

            try:
                score = 0
                selector = None

                element_id = await element.get_attribute("id")
                name = await element.get_attribute("name")
                test_id = await element.get_attribute("data-testid")
                aria_label = await element.get_attribute("aria-label")
                placeholder = await element.get_attribute("placeholder")

                # ------------------------------------------------
                # Build stable selector
                # ------------------------------------------------

                if element_id:
                    selector = f"#{element_id}"

                elif test_id:
                    selector = f'[data-testid="{test_id}"]'

                elif name:
                    selector = f'[name="{name}"]'

                elif aria_label:
                    selector = f'[aria-label="{aria_label}"]'

                elif placeholder:
                    selector = f'[placeholder="{placeholder}"]'

                if selector is None:
                    continue

                # ------------------------------------------------
                # Exact substring matching
                # ------------------------------------------------

                values = [
                    element_id,
                    name,
                    test_id,
                    aria_label,
                    placeholder,
                ]

                values = [
                    str(value).lower()
                    for value in values
                    if value
                ]

                for value in values:

                    if failed_hint and failed_hint in value:
                        score += 10

                # ------------------------------------------------
                # Fuzzy matching
                # ------------------------------------------------

                if failed_hint and values:

                    fuzzy_score = max(
                        SequenceMatcher(
                            None,
                            failed_hint,
                            value,
                        ).ratio()
                        for value in values
                    )

                    logger.debug(
                        f"Healing candidate: "
                        f"{selector} "
                        f"fuzzy={fuzzy_score:.3f}"
                    )

                    if fuzzy_score >= 0.90:
                        score += 10

                    elif fuzzy_score >= 0.80:
                        score += 7

                    elif fuzzy_score >= 0.70:
                        score += 4

                # ------------------------------------------------
                # Form element bonus
                # ------------------------------------------------

                tag_name = await element.evaluate(
                    "(el) => el.tagName.toLowerCase()"
                )

                if tag_name in {
                    "input",
                    "textarea",
                    "select",
                }:
                    score += 1

                # ------------------------------------------------
                # Verify selector is unique
                # ------------------------------------------------

                try:
                    count = await self.page.locator(
                        selector
                    ).count()

                    if count != 1:
                        continue

                except Exception:
                    continue

                # ------------------------------------------------
                # Candidate logging
                # ------------------------------------------------

                logger.info(
                    f"HEAL CANDIDATE -> "
                    f"selector={selector}, "
                    f"id={element_id}, "
                    f"name={name}, "
                    f"aria={aria_label}, "
                    f"placeholder={placeholder}, "
                    f"score={score}"
                )

                # ------------------------------------------------
                # Best candidate
                # ------------------------------------------------

                MIN_HEALING_SCORE = 5

                if (
                    score >= MIN_HEALING_SCORE
                    and score > best_score
                ):
                    best_score = score
                    best_selector = selector

            except Exception as e:

                logger.debug(
                    f"Unable to inspect healing candidate: {e}"
                )

        # --------------------------------------------------------
        # 4. Return best candidate
        # --------------------------------------------------------

        if best_selector:

            logger.success(
                f"Best healed selector: "
                f"{failed_selector} -> "
                f"{best_selector} "
                f"(score={best_score})"
            )

            return best_selector

        # --------------------------------------------------------
        # 5. Nothing found
        # --------------------------------------------------------

        logger.warning(
            f"Unable to heal selector: {failed_selector}"
        )

        return None
