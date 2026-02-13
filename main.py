"""Main entry point that delegates behavior to helpers."""

from helpers.tasks import format_tasks, get_default_tasks


def main() -> None:
    """Orchestrate the flow using helper functions."""
    tasks = get_default_tasks()
    print("Task roadmap:")
    print(format_tasks(tasks))


if __name__ == "__main__":
    main()
