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
