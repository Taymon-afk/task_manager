from models import User


def test_user_creation() -> None:
    user = User(
        user_id=1,
        name="Алексей",
        role="admin",
    )

    assert user.id == 1
    assert user.name == "Алексей"
    assert user.role == "admin"


def test_admin_can_create_tasks() -> None:
    user = User(
        user_id=1,
        name="Алексей",
        role="admin",
    )

    assert user.can_create_tasks()


def test_member_can_create_tasks() -> None:
    user = User(
        user_id=2,
        name="Мария",
        role="member",
    )

    assert user.can_create_tasks()


def test_guest_cannot_create_tasks() -> None:
    user = User(
        user_id=3,
        name="Иван",
        role="guest",
    )

    assert not user.can_create_tasks()


def test_user_string_representation() -> None:
    user = User(
        user_id=1,
        name="Алексей",
        role="admin",
    )

    assert str(user) == "Алексей — роль: admin"
