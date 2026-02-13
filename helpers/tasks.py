"""Task helpers used by the main entry point."""


def get_default_tasks() -> list[str]:
    """Return a simple seed list of tasks."""
    return [
        "Define helper boundaries",
        "Keep main orchestration-only",
        "Add new features by creating new helpers",
    ]


def format_tasks(tasks: list[str]) -> str:
    """Format tasks as a human-readable numbered list."""
    return "\n".join(f"{index}. {task}" for index, task in enumerate(tasks, start=1))
