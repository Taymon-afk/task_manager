from models.task import Task
from models.user import User


class Project:
    """Проект, содержащий задачи."""

    def __init__(
        self,
        project_id: int,
        name: str,
        status: str,
        max_tasks: int,
    ) -> None:
        self.id = project_id
        self.name = name
        self.status = status
        self.max_tasks = max_tasks
        self.tasks: list[Task] = []

    @property
    def current_tasks_count(self) -> int:
        """Возвращает количество задач проекта."""
        return len(self.tasks)

    def can_add_task(
        self,
        user: User,
    ) -> tuple[bool, str]:
        """Проверяет возможность добавления задачи."""
        if self.status != "active":
            return False, "Проект не активен"

        if self.current_tasks_count >= self.max_tasks:
            return False, "Достигнут лимит задач в проекте"

        if not user.can_create_tasks():
            return (
                False,
                "У пользователя нет прав на создание задач",
            )

        return True, "Задача может быть добавлена"

    def add_task(
        self,
        task: Task,
        user: User,
    ) -> tuple[bool, str]:
        """Добавляет задачу в проект после проверки."""
        can_add, reason = self.can_add_task(user)

        if not can_add:
            return False, reason

        for existing_task in self.tasks:
            if existing_task.id == task.id:
                return False, "Задача с таким ID уже существует"

        self.tasks.append(task)
        return True, "Задача успешно добавлена"

    def __str__(self) -> str:
        return (
            f"Проект: {self.name}\n"
            f"Статус: {self.status}\n"
            f"Количество задач: "
            f"{self.current_tasks_count} из {self.max_tasks}"
        )
