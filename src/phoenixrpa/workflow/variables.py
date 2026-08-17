from datetime import date, timedelta
import re


class VariableResolver:

    _DATE_PATTERN = re.compile(
        r"^\{\{(TODAY|YESTERDAY|TOMORROW)([+-]\d+)?\}\}$"
    )

    def __init__(self, variables=None):
        self.variables = variables or {}

    def resolve(self, value):
        if not isinstance(value, str):
            return value

        # Existing workflow variables
        if value.startswith("{{") and value.endswith("}}"):
            variable_name = value[2:-2].strip()

            if variable_name in self.variables:
                return self.variables[variable_name]

        # Dynamic date expressions
        match = self._DATE_PATTERN.match(value.strip())

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
                offset = int(offset_text)
                resolved_date += timedelta(days=offset)

            return resolved_date.isoformat()

        return value
