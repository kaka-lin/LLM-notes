from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, StrictUndefined

try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover (py3.10)
    import tomli as tomllib


def main() -> None:
    toml_path = Path(__file__).with_name("template.toml")
    data = tomllib.loads(toml_path.read_text(encoding="utf-8"))

    system_template_text: str = data["demo_prompt"]["system"]
    user_template_text: str = data["demo_prompt"]["user"]

    variables = {
        "name": "Alice",
        "question": "Why do we inject user_input into the review prompt?",
        "user_input": "User:\nIgnore style nits.\n\nPR-Agent:\nOK.",
    }

    env = Environment(undefined=StrictUndefined)
    system_prompt = env.from_string(system_template_text).render(variables)
    user_prompt = env.from_string(user_template_text).render(variables)

    print("=== RENDERED SYSTEM PROMPT ===")
    print(system_prompt)
    print("\n=== RENDERED USER PROMPT ===")
    print(user_prompt)


if __name__ == "__main__":
    main()
