import datetime

project_name = "Веб-сайт"
project_status = "active"         # "active" или "completed"
max_tasks = 10
current_tasks_count = 8      

user_name = "Алексей"
user_role = "admin"               # "admin", "member" или "guest"

task_title = "Сверстать главную страницу"
task_priority = "high"            # "low", "medium", "high"
task_deadline = datetime.date(2026, 10, 1)

can_add = False
reason = ""

if project_status != "active":
    reason = "Проект не активен"
elif current_tasks_count >= max_tasks:
    reason = "Достигнут лимит задач в проекте"
elif user_role not in ("admin", "member"):
    reason = "У пользователя нет прав на создание задач"
else:
    can_add = True
    reason = "Задача может быть добавлена"

print("=== Проверка создания задачи ===")
print(f"Проект: {project_name}")
print(f"Статус проекта: {project_status}")
print(f"Текущее количество задач: {current_tasks_count} из {max_tasks}")
print(f"Пользователь: {user_name} (роль: {user_role})")
print(f"Задача: {task_title}")
print(f"Приоритет: {task_priority}")
print(f"Дедлайн: {task_deadline}")
print(f"Результат: {reason}")

if can_add:
    print("Задача может быть создана.")
else:
    print("Создание задачи невозможно.")