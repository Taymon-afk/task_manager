from datetime import date

from models import Project, Task, User
from storage import load_all, save_all


def find_user(
    users: list[User],
    user_id: int,
) -> User | None:
    """Ищет пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user

    return None


def find_project(
    projects: list[Project],
    project_id: int,
) -> Project | None:
    """Ищет проект по идентификатору."""
    for project in projects:
        if project.id == project_id:
            return project

    return None


def create_initial_data(
    users: list[User],
    projects: list[Project],
) -> tuple[User, Project]:
    """Создаёт начальные данные, если JSON-файлы пусты."""
    user = find_user(users, 1)

    if user is None:
        user = User(
            user_id=1,
            name="Алексей",
            role="admin",
        )
        users.append(user)

    project = find_project(projects, 1)

    if project is None:
        project = Project(
            project_id=1,
            name="Веб-сайт",
            status="active",
            max_tasks=10,
        )
        projects.append(project)

    return user, project


def find_task(
    project: Project,
    task_id: int,
) -> Task | None:
    """Ищет задачу в проекте по идентификатору."""
    for task in project.tasks:
        if task.id == task_id:
            return task

    return None


def show_projects(projects: list[Project]) -> None:
    """Выводит проекты и находящиеся в них задачи."""
    if not projects:
        print("Проекты отсутствуют.")
        return

    for project in projects:
        print(project)

        if not project.tasks:
            print("В проекте пока нет задач.")
        else:
            for task in project.tasks:
                print()
                print(task)

        print("-" * 40)


def main() -> None:
    """Запускает приложение."""
    users, projects = load_all()

    user, project = create_initial_data(
        users,
        projects,
    )

    existing_task = find_task(
        project=project,
        task_id=1,
    )

    if existing_task is None:
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
    else:
        task_created = False
        message = "Задача уже загружена из JSON"

    print("=== Сервис управления задачами ===")
    print()

    show_projects(projects)

    print()
    print(f"Результат: {message}")

    save_all(
        users=users,
        projects=projects,
    )

    print("Данные сохранены в JSON.")


if __name__ == "__main__":
    main()