from datetime import date

from models import Project, Task, User
from storage import json_storage


def configure_test_files(
    monkeypatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        json_storage,
        "USERS_FILE",
        tmp_path / "users.json",
    )

    monkeypatch.setattr(
        json_storage,
        "PROJECTS_FILE",
        tmp_path / "projects.json",
    )

    monkeypatch.setattr(
        json_storage,
        "TASKS_FILE",
        tmp_path / "tasks.json",
    )


def test_save_and_load_objects(
    monkeypatch,
    tmp_path,
) -> None:
    configure_test_files(
        monkeypatch,
        tmp_path,
    )

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

    project.add_task(task, user)

    json_storage.save_all(
        users=[user],
        projects=[project],
    )

    loaded_users, loaded_projects = (
        json_storage.load_all()
    )

    assert len(loaded_users) == 1
    assert len(loaded_projects) == 1

    loaded_user = loaded_users[0]
    loaded_project = loaded_projects[0]

    assert loaded_user.name == "Алексей"
    assert loaded_project.name == "Веб-сайт"
    assert len(loaded_project.tasks) == 1

    loaded_task = loaded_project.tasks[0]

    assert loaded_task.title == (
        "Сверстать главную страницу"
    )
    assert loaded_task.deadline == date(2026, 10, 1)
    assert loaded_task.assignee is loaded_user


def test_load_missing_files(
    monkeypatch,
    tmp_path,
) -> None:
    configure_test_files(
        monkeypatch,
        tmp_path,
    )

    users, projects = json_storage.load_all()

    assert users == []
    assert projects == []
