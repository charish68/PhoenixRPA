import operator


class ConditionEvaluator:
    OPERATORS = {
        "==": operator.eq,
        "!=": operator.ne,
    }

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