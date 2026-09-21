from datetime import date

from models import Project, Task, User


def main() -> None:
    """Запускает демонстрационный сценарий приложения."""
    user = User(
        user_id=1,
        name="Алексей",
        role="admin",
    )

    project = Project(
        project_id=1,
        name="Веб-сайт",
        status="active",
        max_tasks=10,
    )

    task = Task(
        task_id=1,
        title="Сверстать главную страницу",
        assignee=user,
        priority="high",
        deadline=date(2026, 10, 1),
    )

    task_created, message = project.add_task(
        task=task,
        user=user,
    )

    print("=== Сервис управления задачами ===")
    print(project)
    print()

    if task_created:
        print(task)
        print()

    print(f"Результат: {message}")


if __name__ == "__main__":
    main()