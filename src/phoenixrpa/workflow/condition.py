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
        return self.OPERATORS[op](left, right)