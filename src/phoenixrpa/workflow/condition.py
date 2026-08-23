import operator


class ConditionEvaluator:
    OPERATORS = {
        "==": operator.eq,
        "!=": operator.ne,
    }

    def parse(
        self,
        condition: str,
    ) -> tuple[str, str, str]:
        for operator_symbol in self.OPERATORS:
            if operator_symbol in condition:
                left, right = condition.split(
                    operator_symbol,
                    maxsplit=1,
                )

                if not left.strip() or not right.strip():
                    raise ValueError(
                        "Condition must contain left operator right."
                    )

                return (
                    left.strip(),
                    operator_symbol,
                    right.strip(),
                )

        parts = condition.split(maxsplit=2)

        if len(parts) == 3:
            raise ValueError(
                f"unsupported condition operator: {parts[1]}"
            )

        raise ValueError(
            "Condition must contain left operator right."
        )

    def evaluate(
        self,
        left: str,
        op: str,
        right: str,
    ) -> bool:
        if op not in self.OPERATORS:
            raise ValueError(
                f"Unsupported condition operator: {op}"
            )

        return self.OPERATORS[op](left, right)