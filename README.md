# 📸 PhotoShare API

REST API сервіс для завантаження, зберігання та управління фотографіями з системою тегів, коментарів, ролей користувачів та інтеграцією з Cloudinary.

---

## 🛠 Стек технологій

- **Python 3.14+**
- **FastAPI** — асинхронний вебфреймворк
- **SQLAlchemy 2.0** (AsyncSession) — ORM
- **PostgreSQL** — основна база даних
- **Alembic** — міграції БД
- **Poetry** — управління залежностями та віртуальним оточенням
- **Cloudinary** — зберігання зображень
- **JWT** (python-jose) — авторизація
- **Passlib + bcrypt** — хешування паролів
- **Pydantic v2** — валідація даних
- **QR-code** — генерація QR-кодів для фото
- **Pytest + pytest-asyncio** — тестування

---

## 📋 Вимоги

- Python 3.14 або вище
- PostgreSQL (локально або віддалено)
- Poetry — менеджер залежностей

---

## 🚀 Локальний запуск

### 1. Клонування репозиторію

```bash
git clone <посилання-на-твій-репозиторій>
cd Project_goit
```

### 2. Встановлення Poetry (якщо ще не встановлено)

**Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### 3. Встановлення залежностей

```bash
poetry install
```

> Ця команда автоматично створить віртуальне оточення та встановить усі залежності з `pyproject.toml`. Окремо створювати `python -m venv` не потрібно — Poetry робить це сам.

### 4. Налаштування змінних оточення

Створіть у кореневій папці проєкту файл `.env`:

```env
# База даних
DB_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/photoshare

# JWT авторизація
SECRET_KEY=your-super-secret-key-change-me
ALGORITHM=HS256

# Cloudinary
CLOUDINARY_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 5. Застосування міграцій бази даних

```bash
poetry run alembic upgrade head
```

### 6. Запуск сервера

**Варіант А — через `poetry run` (рекомендовано):**
```bash
poetry run uvicorn main:app --reload
```

**Варіант Б — через активоване оточення:**
```bash
poetry env activate
uvicorn main:app --reload
```

Після запуску API буде доступне за адресою: **http://127.0.0.1:8000**

---

## ☁️ Деплой на Fly.io

Проєкт задеплоєний на [Fly.io](https://fly.io) і доступний за адресою:
**https://projectgoit.fly.dev**

### Встановлення Fly CLI

**Windows (PowerShell):**
```powershell
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

Після встановлення авторизуйтесь:
```bash
fly auth login
```

### Перший деплой

Якщо додаток ще не створено на Fly:

```bash
fly launch
```

Це створить `fly.toml` та запитає базові налаштування (регіон, назву додатку, чи потрібна база даних тощо).

### Конфігурація (`fly.toml`)

```toml
app = 'projectgoit'
primary_region = 'fra'

[build]

[deploy]
  release_command = "alembic upgrade head"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ['app']
```

- `release_command` — автоматично застосовує міграції Alembic **перед** кожним деплоєм нової версії.
- `auto_stop_machines` / `auto_start_machines` — машина сама "засинає" при простої та "прокидається" при вхідному запиті, вручну нічого запускати не потрібно.

### Змінні оточення (secrets)

Замість `.env`-файлу на проді використовуються Fly secrets:

```bash
fly secrets set DB_URL="postgresql+asyncpg://user:password@host:5432/dbname" \
  SECRET_KEY="your-super-secret-key" \
  ALGORITHM="HS256" \
  CLOUDINARY_NAME="your_cloud_name" \
  CLOUDINARY_API_KEY="your_api_key" \
  CLOUDINARY_API_SECRET="your_api_secret" \
  -a projectgoit
```

### Деплой оновлень

Після будь-яких змін у коді:

```bash
fly deploy
```

Fly сам збере новий Docker-образ, застосує міграції (`release_command`) і викотить нову версію. Нічого запускати чи зупиняти вручну не треба.

### Корисні команди

| Команда | Що робить |
|---|---|
| `fly status -a projectgoit` | Перевірити стан застосунку та машин |
| `fly logs -a projectgoit` | Переглянути логи в реальному часі |
| `fly ssh console -a projectgoit` | Зайти всередину контейнера (для дебагу) |
| `fly machine start <id> -a projectgoit` | Запустити конкретну машину вручну |
| `fly secrets list -a projectgoit` | Переглянути список змінних оточення |

### Документація API на проді

- Swagger UI: **https://projectgoit.fly.dev/docs**
- ReDoc: **https://projectgoit.fly.dev/redoc**

---

## 📖 Локальна документація API

Після запуску сервера локально відкрийте у браузері:

- **Swagger UI** (інтерактивна документація з можливістю тестування): http://127.0.0.1:8000/docs
- **ReDoc** (альтернативний, більш читабельний вигляд): http://127.0.0.1:8000/redoc

---

## 🧪 Тестування

Для запуску всіх тестів:

```bash
poetry run pytest -v
```

---

## 📂 Структура проєкту

```
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
├── alembic.ini          # Конфігурація Alembic
├── fly.toml             # Конфігурація деплою на Fly.io
├── Dockerfile            # Docker-образ для деплою
├── main.py               # Точка входу додатку
├── pyproject.toml        # Залежності Poetry
├── .env                  # Змінні оточення (не комітити!)
└── README.md
```

---

## 🔑 Основні можливості

- ✅ Реєстрація та авторизація користувачів (JWT)
- ✅ Завантаження фото у Cloudinary
- ✅ Система тегів (без дублікатів)
- ✅ Коментарі до фото
- ✅ Ролі користувачів (звичайний користувач / адміністратор)
- ✅ Генерація QR-кодів для фото