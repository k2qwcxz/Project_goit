📸 PhotoShare API
REST API сервіс для завантаження, зберігання та управління фотографіями з системою тегів, коментарів, ролей користувачів та інтеграцією з Cloudinary.

🛠 Стек технологій
Python 3.14+
FastAPI — асинхронний вебфреймворк
SQLAlchemy 2.0 (AsyncSession) — ORM
PostgreSQL — основна база даних
Alembic — міграції БД
Poetry — управління залежностями та віртуальним оточенням
Cloudinary — зберігання зображень
JWT (python-jose) — авторизація
Passlib + bcrypt — хешування паролів
Pydantic v2 — валідація даних
QR-code — генерація QR-кодів для фото
Pytest + pytest-asyncio — тестування


📋 Вимоги
Python 3.14 або вище
PostgreSQL (локально або віддалено)
Poetry — менеджер залежностей

🚀 Встановлення та запуск
1. Клонювання репозиторію
git clone <посилання-на-твій-репозиторій>
cd Project_goit

2. Встановлення Poetry (якщо ще не встановлено)
Windows (PowerShell):
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

3. Встановлення залежностей та створення віртуального оточення
poetry install
"Ця команда автоматично створить віртуальне оточення та встановить усі залежності з pyproject.toml. Окремо створювати python -m venv не потрібно — Poetry робить це сам."

4. Налаштування змінних оточення
Створіть у кореневій папці проєкту файл .env з таким вмістом:

# База даних
DB_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/photoshare

# JWT авторизація
SECRET_KEY=your-super-secret-key-change-me
ALGORITHM=HS256

# Cloudinary
CLOUDINARY_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

5. Застосування міграцій бази даних
poetry run alembic upgrade head

6. Запуск сервера
Є два варіанти:

Варіант А — через poetry run (рекомендовано):
poetry run uvicorn main:app --reload

Варіант Б — через poetry env activate:
env activate
uvicorn main:app --reload

Після запуску API буде доступне за адресою: http://127.0.0.1:8000

📖 Документація API
Після запуску сервера відкрийте у браузері:
Swagger UI (інтерактивна документація з можливістю тестування): http://127.0.0.1:8000/docs
ReDoc (альтернативний, більш читабельний вигляд): http://127.0.0.1:8000/redoc

🧪 Тестування
Для запуску всіх тестів:
poetry run pytest -v


📂 Структура проєкту
Project_goit/
├── PhotoShare/
│   ├── conf/           # Конфігураційні файли проєкту
│   ├── database/       # Моделі SQLAlchemy, налаштування сесій
│   ├── repository/     # Шар роботи з даними (CRUD)
│   ├── services/       # Бізнес-логіка (JWT, хешування, Cloudinary)
│   ├── routers/        # Ендпоінти (маршрути) API
│   ├── schemas/        # Pydantic-схеми для валідації
│   └── tests/          # Тести (pytest)
├── alembic/            # Міграції бази даних
├── alembic.ini         # Конфігурація Alembic
├── main.py             # Точка входу додатку
├── pyproject.toml      # Залежності Poetry
├── .env                # Змінні оточення (не комітити!)
└── README.md

🔑 Основні можливості
✅ Реєстрація та авторизація користувачів (JWT)
✅ Завантаження фото у Cloudinary
✅ Система тегів (без дублікатів)
✅ Коментарі до фото
✅ Ролі користувачів (звичайний користувач / адміністратор)
✅ Генерація QR-кодів для фото

