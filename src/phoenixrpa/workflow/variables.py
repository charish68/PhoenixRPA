import re


class VariableResolver:
    def __init__(self, variables: dict[str, str] | None = None):
        self.variables = variables or {}

    def resolve(
        self,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        pattern = r"\$\{([^}]+)\}"

        def replace(match):
            key = match.group(1)
            return str(self.variables.get(key, match.group(0)))

        return re.sub(
            pattern,
            replace,
            value,
        )

    def set(
        self,
        key: str,
        value: str,
    ):
        self.variables[key] = value

    def get(
        self,
        key: str,
    ):
        return self.variables.get(key)