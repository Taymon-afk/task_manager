from datetime import date

from models import Project, Task, User
from storage import load_all, save_all


def input_int(prompt: str) -> int:
    """Запрашивает положительное целое число."""
    while True:
        try:
            value = int(input(prompt))

            if value <= 0:
                print("Введите число больше нуля.")
                continue

            return value
        except ValueError:
            print("Ошибка: необходимо ввести целое число.")


def input_text(prompt: str) -> str:
    """Запрашивает непустую строку."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Значение не может быть пустым.")


def input_date(prompt: str) -> date:
    """Запрашивает дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = input(prompt).strip()

        try:
            return date.fromisoformat(value)
        except ValueError:
            print(
                "Некорректная дата. "
                "Используйте формат ГГГГ-ММ-ДД."
            )


def input_role() -> str:
    """Запрашивает роль пользователя."""
    allowed_roles = ("admin", "member", "guest")

    while True:
        role = input(
            "Роль (admin/member/guest): "
        ).strip().lower()

        if role in allowed_roles:
            return role

        print(
            "Допустимые роли: admin, member, guest."
        )


def input_priority() -> str:
    """Запрашивает приоритет задачи."""
    allowed_priorities = ("high", "medium", "low")

    while True:
        priority = input(
            "Приоритет (high/medium/low): "
        ).strip().lower()

        if priority in allowed_priorities:
            return priority

        print(
            "Допустимые приоритеты: "
            "high, medium, low."
        )


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


def find_task(
    project: Project,
    task_id: int,
) -> Task | None:
    """Ищет задачу в проекте."""
    for task in project.tasks:
        if task.id == task_id:
            return task

    return None


def get_next_user_id(users: list[User]) -> int:
    """Возвращает следующий ID пользователя."""
    if not users:
        return 1

    return max(user.id for user in users) + 1


def get_next_project_id(
    projects: list[Project],
) -> int:
    """Возвращает следующий ID проекта."""
    if not projects:
        return 1

    return max(project.id for project in projects) + 1


def get_next_task_id(
    projects: list[Project],
) -> int:
    """Возвращает следующий ID задачи."""
    task_ids = [
        task.id
        for project in projects
        for task in project.tasks
    ]

    if not task_ids:
        return 1

    return max(task_ids) + 1


def create_initial_data(
    users: list[User],
    projects: list[Project],
) -> None:
    """Создаёт демонстрационные данные при первом запуске."""
    if users or projects:
        return

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

    users.append(user)
    projects.append(project)
    project.add_task(task, user)


def show_users(users: list[User]) -> None:
    """Выводит список пользователей."""
    print("\n=== Пользователи ===")

    if not users:
        print("Пользователи отсутствуют.")
        return

    for user in users:
        print(f"ID: {user.id}. {user}")


def show_projects(projects: list[Project]) -> None:
    """Выводит проекты и их задачи."""
    print("\n=== Проекты и задачи ===")

    if not projects:
        print("Проекты отсутствуют.")
        return

    for project in projects:
        print()
        print(project)

        if not project.tasks:
            print("Задачи отсутствуют.")
        else:
            for task in project.tasks:
                print()
                print(task)

        print("-" * 40)


def add_user(users: list[User]) -> None:
    """Создаёт нового пользователя."""
    print("\n=== Добавление пользователя ===")

    name = input_text("Имя пользователя: ")
    role = input_role()

    user = User(
        user_id=get_next_user_id(users),
        name=name,
        role=role,
    )

    users.append(user)

    print("Пользователь успешно добавлен.")
    print(user)


def add_project(projects: list[Project]) -> None:
    """Создаёт новый проект."""
    print("\n=== Добавление проекта ===")

    name = input_text("Название проекта: ")
    max_tasks = input_int(
        "Максимальное количество задач: "
    )

    project = Project(
        project_id=get_next_project_id(projects),
        name=name,
        status="active",
        max_tasks=max_tasks,
    )

    projects.append(project)

    print("Проект успешно добавлен.")
    print(project)


def add_task(
    users: list[User],
    projects: list[Project],
) -> None:
    """Создаёт задачу и добавляет её в проект."""
    print("\n=== Добавление задачи ===")

    if not users:
        print(
            "Сначала необходимо создать пользователя."
        )
        return

    if not projects:
        print(
            "Сначала необходимо создать проект."
        )
        return

    show_projects(projects)
    project_id = input_int("Введите ID проекта: ")

    project = find_project(projects, project_id)

    if project is None:
        print("Проект с таким ID не найден.")
        return

    show_users(users)
    user_id = input_int(
        "Введите ID исполнителя: "
    )

    user = find_user(users, user_id)

    if user is None:
        print("Пользователь с таким ID не найден.")
        return

    title = input_text("Название задачи: ")
    priority = input_priority()
    deadline = input_date(
        "Дедлайн в формате ГГГГ-ММ-ДД: "
    )

    task = Task(
        task_id=get_next_task_id(projects),
        title=title,
        assignee=user,
        priority=priority,
        deadline=deadline,
    )

    task_created, message = project.add_task(
        task=task,
        user=user,
    )

    print(message)

    if task_created:
        print(task)


def complete_task(projects: list[Project]) -> None:
    """Отмечает выбранную задачу как выполненную."""
    print("\n=== Завершение задачи ===")

    if not projects:
        print("Проекты отсутствуют.")
        return

    show_projects(projects)
    project_id = input_int("Введите ID проекта: ")

    project = find_project(projects, project_id)

    if project is None:
        print("Проект с таким ID не найден.")
        return

    if not project.tasks:
        print("В выбранном проекте нет задач.")
        return

    task_id = input_int("Введите ID задачи: ")
    task = find_task(project, task_id)

    if task is None:
        print("Задача с таким ID не найдена.")
        return

    if task.is_completed:
        print("Эта задача уже выполнена.")
        return

    task.complete()
    print("Задача отмечена как выполненная.")


def show_menu() -> None:
    """Выводит главное меню."""
    print("\n=== Сервис управления задачами ===")
    print("1. Показать пользователей")
    print("2. Показать проекты и задачи")
    print("3. Добавить пользователя")
    print("4. Добавить проект")
    print("5. Добавить задачу")
    print("6. Завершить задачу")
    print("0. Сохранить данные и выйти")


def main() -> None:
    """Запускает консольное приложение."""
    users, projects = load_all()

    create_initial_data(users, projects)
    save_all(users, projects)

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_users(users)
        elif choice == "2":
            show_projects(projects)
        elif choice == "3":
            add_user(users)
            save_all(users, projects)
        elif choice == "4":
            add_project(projects)
            save_all(users, projects)
        elif choice == "5":
            add_task(users, projects)
            save_all(users, projects)
        elif choice == "6":
            complete_task(projects)
            save_all(users, projects)
        elif choice == "0":
            save_all(users, projects)
            print("Данные сохранены.")
            print("Работа программы завершена.")
            break
        else:
            print("Такого пункта меню нет.")


if __name__ == "__main__":
    main()
