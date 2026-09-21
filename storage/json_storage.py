import json
from datetime import date
from pathlib import Path
from typing import Any

from models import Project, Task, User


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

USERS_FILE = DATA_DIR / "users.json"
PROJECTS_FILE = DATA_DIR / "projects.json"
TASKS_FILE = DATA_DIR / "tasks.json"


def read_json(file_path: Path) -> list[dict[str, Any]]:
    """Читает список словарей из JSON-файла."""
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        print(
            f"Не удалось прочитать файл {file_path.name}: "
            f"{error}"
        )
        return []

    if not isinstance(data, list):
        print(
            f"Файл {file_path.name} должен содержать список."
        )
        return []

    return [
        item
        for item in data
        if isinstance(item, dict)
    ]


def write_json(
    file_path: Path,
    data: list[dict[str, Any]],
) -> None:
    """Записывает список словарей в JSON-файл."""
    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )


def load_users() -> list[User]:
    """Загружает пользователей из JSON."""
    users: list[User] = []

    for item in read_json(USERS_FILE):
        try:
            user = User(
                user_id=int(item["id"]),
                name=str(item["name"]),
                role=str(item["role"]),
            )
        except (KeyError, TypeError, ValueError) as error:
            print(
                "Пропущена некорректная запись "
                f"пользователя: {error}"
            )
            continue

        users.append(user)

    return users


def save_users(users: list[User]) -> None:
    """Сохраняет пользователей в JSON."""
    data = []

    for user in users:
        data.append(
            {
                "id": user.id,
                "name": user.name,
                "role": user.role,
            }
        )

    write_json(USERS_FILE, data)


def load_projects() -> list[Project]:
    """Загружает проекты из JSON."""
    projects: list[Project] = []

    for item in read_json(PROJECTS_FILE):
        try:
            project = Project(
                project_id=int(item["id"]),
                name=str(item["name"]),
                status=str(item["status"]),
                max_tasks=int(item["max_tasks"]),
            )
        except (KeyError, TypeError, ValueError) as error:
            print(
                "Пропущена некорректная запись "
                f"проекта: {error}"
            )
            continue

        projects.append(project)

    return projects


def save_projects(projects: list[Project]) -> None:
    """Сохраняет проекты в JSON."""
    data = []

    for project in projects:
        data.append(
            {
                "id": project.id,
                "name": project.name,
                "status": project.status,
                "max_tasks": project.max_tasks,
            }
        )

    write_json(PROJECTS_FILE, data)


def load_tasks(
    projects: list[Project],
    users: list[User],
) -> None:
    """Загружает задачи и связывает их с объектами."""
    projects_by_id = {
        project.id: project
        for project in projects
    }

    users_by_id = {
        user.id: user
        for user in users
    }

    for item in read_json(TASKS_FILE):
        try:
            project_id = int(item["project_id"])
            assignee_id = int(item["assignee_id"])

            project = projects_by_id.get(project_id)
            assignee = users_by_id.get(assignee_id)

            if project is None:
                print(
                    "Пропущена задача: проект "
                    f"с ID {project_id} не найден."
                )
                continue

            if assignee is None:
                print(
                    "Пропущена задача: пользователь "
                    f"с ID {assignee_id} не найден."
                )
                continue

            task = Task(
                task_id=int(item["id"]),
                title=str(item["title"]),
                assignee=assignee,
                priority=str(item["priority"]),
                deadline=date.fromisoformat(
                    str(item["deadline"])
                ),
            )

            task.is_completed = bool(
                item.get("is_completed", False)
            )
        except (KeyError, TypeError, ValueError) as error:
            print(
                "Пропущена некорректная запись "
                f"задачи: {error}"
            )
            continue

        project.tasks.append(task)


def save_tasks(projects: list[Project]) -> None:
    """Сохраняет задачи всех проектов в JSON."""
    data = []

    for project in projects:
        for task in project.tasks:
            data.append(
                {
                    "id": task.id,
                    "project_id": project.id,
                    "title": task.title,
                    "assignee_id": task.assignee.id,
                    "priority": task.priority,
                    "deadline": task.deadline.isoformat(),
                    "is_completed": task.is_completed,
                }
            )

    write_json(TASKS_FILE, data)


def load_all() -> tuple[list[User], list[Project]]:
    """Загружает все данные приложения."""
    users = load_users()
    projects = load_projects()
    load_tasks(projects, users)

    return users, projects


def save_all(
    users: list[User],
    projects: list[Project],
) -> None:
    """Сохраняет все данные приложения."""
    save_users(users)
    save_projects(projects)
    save_tasks(projects)