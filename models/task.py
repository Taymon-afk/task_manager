from datetime import date

from models.user import User


class Task:
    """Задача, назначенная пользователю."""

    def __init__(
        self,
        task_id: int,
        title: str,
        assignee: User,
        priority: str,
        deadline: date,
    ) -> None:
        self.id = task_id
        self.title = title
        self.assignee = assignee
        self.priority = priority
        self.deadline = deadline
        self.is_completed = False

    def get_priority_label(self) -> str:
        """Возвращает понятное название приоритета."""
        priority_labels = {
            "high": "Высокий приоритет",
            "medium": "Средний приоритет",
            "low": "Низкий приоритет",
        }

        return priority_labels.get(
            self.priority,
            "Приоритет не определён",
        )

    def complete(self) -> None:
        """Отмечает задачу как выполненную."""
        self.is_completed = True

    def __str__(self) -> str:
        if self.is_completed:
            status = "Выполнена"
        else:
            status = "В работе"

        return (
            f"Задача №{self.id}: {self.title}\n"
            f"Исполнитель: {self.assignee.name}\n"
            f"{self.get_priority_label()}\n"
            f"Дедлайн: {self.deadline:%d.%m.%Y}\n"
            f"Статус: {status}"
        )
