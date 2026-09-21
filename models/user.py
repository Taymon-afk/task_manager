class User:
    """Пользователь сервиса управления задачами."""

    def __init__(
        self,
        user_id: int,
        name: str,
        role: str,
    ) -> None:
        self.id = user_id
        self.name = name
        self.role = role

    def can_create_tasks(self) -> bool:
        """Проверяет право пользователя на создание задач."""
        return self.role in ("admin", "member")

    def __str__(self) -> str:
        return f"{self.name} — роль: {self.role}"
