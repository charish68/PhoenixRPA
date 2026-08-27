from datetime import date, timedelta

from phoenixrpa.workflow.variables import VariableResolver


def test_resolves_today():
    resolver = VariableResolver()

    result = resolver.resolve("{{TODAY}}")

    assert result == date.today().isoformat()


def test_resolves_yesterday():
    resolver = VariableResolver()

    result = resolver.resolve("{{YESTERDAY}}")

    assert result == (
        date.today() - timedelta(days=1)
    ).isoformat()


def test_resolves_tomorrow():
    resolver = VariableResolver()

    result = resolver.resolve("{{TOMORROW}}")

    assert result == (
        date.today() + timedelta(days=1)
    ).isoformat()


def test_resolves_today_minus_days():
    resolver = VariableResolver()

    result = resolver.resolve("{{TODAY-7}}")

    assert result == (
        date.today() - timedelta(days=7)
    ).isoformat()


def test_resolves_today_plus_days():
    resolver = VariableResolver()

    result = resolver.resolve("{{TODAY+7}}")

    assert result == (
        date.today() + timedelta(days=7)
    ).isoformat()


def test_static_value_is_unchanged():
    resolver = VariableResolver()

    assert resolver.resolve("hello") == "hello"
    assert resolver.resolve("12345") == "12345"

def test_resolves_stored_variable():
    resolver = VariableResolver()
    resolver.set("username", "charish")

    assert resolver.resolve("{{username}}") == "charish"


def test_unknown_variable_is_unchanged():
    resolver = VariableResolver()

    assert resolver.resolve(
        "{{unknown_variable}}"
    ) == "{{unknown_variable}}"


def test_non_string_value_is_unchanged():
    resolver = VariableResolver()

    assert resolver.resolve(123) == 123
    assert resolver.resolve(None) is None


def test_resolves_yesterday_plus_days():
    resolver = VariableResolver()

    result = resolver.resolve("{{YESTERDAY+3}}")

    assert result == (
        date.today() + timedelta(days=2)
    ).isoformat()


def test_resolves_tomorrow_minus_days():
    resolver = VariableResolver()

    result = resolver.resolve("{{TOMORROW-3}}")

    assert result == (
        date.today() - timedelta(days=2)
    ).isoformat()

def test_resolves_embedded_variable():
    resolver = VariableResolver()
    resolver.set("name", "Rahul")

    result = resolver.resolve(
        "Hello {{name}}"
    )

    assert result == "Hello Rahul"


def test_resolves_multiple_embedded_variables():
    resolver = VariableResolver()
    resolver.set("first_name", "Rahul")
    resolver.set("last_name", "Kumar")

    result = resolver.resolve(
        "{{first_name}} {{last_name}}"
    )

    assert result == "Rahul Kumar"