from datetime import date, timedelta
import re


class VariableResolver:

    _DATE_PATTERN = re.compile(
        r"^\{\{(TODAY|YESTERDAY|TOMORROW)([+-]\d+)?\}\}$"
    )

    _VARIABLE_PATTERN = re.compile(
        r"^\{\{([^{}]+)\}\}$"
    )

    _EMBEDDED_VARIABLE_PATTERN = re.compile(
        r"\{\{([^{}]+)\}\}"
    )

    def __init__(self, variables=None):
        self.variables = variables or {}

    def resolve(self, value):
        if not isinstance(value, str):
            return value

        # Preserve the original object when the entire value
        # is exactly one workflow variable.
        variable_match = self._VARIABLE_PATTERN.fullmatch(
            value.strip()
        )

        if variable_match:
            variable_name = variable_match.group(1).strip()

            if variable_name in self.variables:
                return self.variables[variable_name]

        # Dynamic date expressions
        match = self._DATE_PATTERN.fullmatch(
            value.strip()
        )

        if match:
            keyword = match.group(1)
            offset_text = match.group(2)

            today = date.today()

            if keyword == "TODAY":
                resolved_date = today
            elif keyword == "YESTERDAY":
                resolved_date = today - timedelta(days=1)
            else:
                resolved_date = today + timedelta(days=1)

            if offset_text:
                resolved_date += timedelta(
                    days=int(offset_text)
                )

            return resolved_date.isoformat()

        # Replace variables embedded inside text.
        def replace_variable(match):
            variable_name = match.group(1).strip()

            if variable_name in self.variables:
                return str(
                    self.variables[variable_name]
                )

            return match.group(0)

        return self._EMBEDDED_VARIABLE_PATTERN.sub(
            replace_variable,
            value,
        )

    def set(
        self,
        name: str,
        value,
    ):
        self.variables[name] = value
