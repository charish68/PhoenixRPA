import asyncio
from difflib import SequenceMatcher

from playwright.async_api import Page

from phoenixrpa.agents.healing_agent import AIHealingAgent
from phoenixrpa.healing.models import HealingResult
from phoenixrpa.core.logger import logger


class HealingService:

    def __init__(
        self,
        page: Page,
        ai_agent: AIHealingAgent | None = None,
    ):
        self.page = page
        self.ai_agent = ai_agent
        self.last_failure_reason: str | None = None

    async def _validate_selector(
        self,
        selector: str,
    ) -> bool:
        """
        Validate that an AI-generated selector is valid,
        resolves successfully, and identifies exactly one element.
        """

        if not selector:
            return False

        try:
            count = await self.page.locator(selector).count()

            if count != 1:
                logger.warning(
                    f"AI selector rejected: "
                    f"{selector} (matches {count} elements)"
                )
                return False

            return True

        except Exception as e:
            logger.warning(
                f"AI selector validation failed: "
                f"{selector} -> {e}"
            )
            return False

    async def _ai_heal(
        self,
        failed_selector: str,
    ) -> str | None:
        """
        Ask the AI healing agent for a selector and
        validate the result before returning it.
        """

        if self.ai_agent is None:
            self.last_failure_reason = "NO_AI_AGENT"
            logger.info(
                "AI healing is not configured."
            )
            return None

        try:
            page_context = await self.page.locator(
                "body"
            ).inner_text()

            logger.info(
                f"Attempting AI selector healing for: "
                f"{failed_selector}"
            )

            suggested_selector = await asyncio.wait_for(
                self.ai_agent.suggest_selector(
                    failed_selector,
                    page_context,
                ),
                timeout=30.0,
            )

            if not suggested_selector:
                self.last_failure_reason = "AI_NO_SELECTOR"
                logger.warning(
                    "AI healing returned no selector."
                )
                return None

            suggested_selector = (
                suggested_selector.strip()
            )

            # Remove accidental markdown code fences.
            if suggested_selector.startswith("```"):
                suggested_selector = (
                    suggested_selector
                    .replace("```css", "")
                    .replace("```", "")
                    .strip()
                )

            logger.info(
                f"AI suggested selector: "
                f"{suggested_selector}"
            )

            if not await self._validate_selector(
                suggested_selector
            ):
                self.last_failure_reason = "AI_VALIDATION_FAILED"
                logger.warning(
                    "AI suggested selector failed "
                    "Playwright validation."
                )
                return None

            logger.success(
                f"AI selector healed: "
                f"{failed_selector} -> "
                f"{suggested_selector}"
            )

            return suggested_selector

        except Exception as e:
            self.last_failure_reason = "AI_EXCEPTION"
            logger.exception(
                f"AI healing failed: {e}"
            )
            return None

    async def find_best_selector(
        self,
        failed_selector: str,
        return_result: bool = False,
    ) -> str | HealingResult | None:

        logger.info(
            f"Attempting selector healing for: "
            f"{failed_selector}"
        )

        # --------------------------------------------------------
        # 1. Check whether original selector still exists
        # --------------------------------------------------------

        try:
            locator = self.page.locator(
                failed_selector
            )

            if await locator.count() > 0:
                logger.info(
                    f"Original selector still exists: "
                    f"{failed_selector}"
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

                element_id = await element.get_attribute(
                    "id"
                )
                name = await element.get_attribute(
                    "name"
                )
                test_id = await element.get_attribute(
                    "data-testid"
                )
                aria_label = await element.get_attribute(
                    "aria-label"
                )
                placeholder = await element.get_attribute(
                    "placeholder"
                )

                # ------------------------------------------------
                # Build stable selector
                # ------------------------------------------------

                if element_id:
                    selector = f"#{element_id}"

                elif test_id:
                    selector = (
                        f'[data-testid="{test_id}"]'
                    )

                elif name:
                    selector = (
                        f'[name="{name}"]'
                    )

                elif aria_label:
                    selector = (
                        f'[aria-label="{aria_label}"]'
                    )

                elif placeholder:
                    selector = (
                        f'[placeholder="{placeholder}"]'
                    )

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

                    if (
                        failed_hint
                        and failed_hint in value
                    ):
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
                    f"Unable to inspect healing "
                    f"candidate: {e}"
                )

        # --------------------------------------------------------
        # 4. Deterministic healing succeeded
        # --------------------------------------------------------

        if best_selector:

            logger.success(
                f"Best healed selector: "
                f"{failed_selector} -> "
                f"{best_selector} "
                f"(score={best_score})"
            )

            confidence = min(
                best_score / 21.0,
                1.0,
            )

            result = HealingResult(
                status="HEALED",
                original_selector=failed_selector,
                healed_selector=best_selector,
                method="DETERMINISTIC",
                confidence=confidence,
            )

            return result if return_result else best_selector

        # --------------------------------------------------------
        # 5. AI healing fallback
        # --------------------------------------------------------

        logger.warning(
            f"Deterministic healing failed for: "
            f"{failed_selector}"
        )

        self.last_failure_reason = None

        ai_selector = await self._ai_heal(
            failed_selector
        )

        if ai_selector:
            result = HealingResult(
                status="HEALED",
                original_selector=failed_selector,
                healed_selector=ai_selector,
                method="AI",
                confidence=1.0,
            )

            return result if return_result else ai_selector
        # --------------------------------------------------------
        # 6. Nothing found
        # --------------------------------------------------------

        logger.warning(
            f"Unable to heal selector: "
            f"{failed_selector}"
        )

        if return_result:
            return HealingResult(
                status="FAILED",
                original_selector=failed_selector,
                method="AI",
                failure_reason=(
                    self.last_failure_reason
                    or "DETERMINISTIC_NO_MATCH"
                ),
            )

        return None
