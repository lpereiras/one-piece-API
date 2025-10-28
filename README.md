# One Piece API 🏴‍☠️

> Made by a big fan of the Straw Hat crew, besides a curious and proactive QA Engineer! :)

## 📖 About The Project

The project aims to demystify the SDLC (Software Development Life Cycle) by building an API from scratch. Through this, I aim to gain a deeper understanding of the software I'll test and automate in real-world workflows.

## 🛠️ Tech Stack

![Poetry](https://img.shields.io/badge/Poetry-60A5FA.svg?style=for-the-badge&logo=Poetry&logoColor=white)
![PyTest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style=for-the-badge&logo=Pytest&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=for-the-badge&logo=FastAPI&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=for-the-badge&logo=SQLAlchemy&logoColor=white)

## 🚀 Getting Started

> [!NOTE]  
> To install and run the project tests, make sure you have the following:
> | Required | Recommended version |
> | ------------- |:-------------:|
> | Poetry | ^2.0 |
> | pytest | ^8.4.1 |
> | Python3 | 3.13 |

To verify your installations:

```bash
python3 --version  # Should be 3.13 or higher
poetry --version   # Should be 2.0 or higher
```

### Installation

1. **Fork the repository**

   Click the "Fork" button at the top right of the repository page to create your own copy.

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR-USERNAME/one-piece-API.git
   cd one-piece-API
   ```

3. **Install dependencies**

   ```bash
   poetry install
   ```

   This will create a virtual environment and install all required packages.

4. **Set up environment variables**

   Create a `.env` file in the root directory with the following variables:

   ```env
   DATABASE_URL=sqlite:///database.db
   ALGORITHM=HS256
   SECRET_KEY=your-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   ```

5. **Run database migrations**

   ```bash
   poetry run alembic upgrade head
   ```

   This will create the database tables.

6. **Start the development server**

   ```bash
   poetry run task dev
   ```

   The API will be available at: `http://127.0.0.1:8000`

7. **Access the interactive API documentation**

   - Swagger UI: `http://127.0.0.1:8000/docs`

## 📚 API Endpoints

### Authentication

- `POST /auth/token`
- `POST /auth/refresh-token`

### Users

- `POST /users/`
- `GET /users/`
- `GET /users/{user_id}`
- `DELETE /users/{user_id}`

### Devil Fruits

:construction: **in progress** :construction:

### Version

- `GET /version`

## 🧪 Running Tests

Run all tests with coverage:

```bash
poetry run task test
```

Run a specific test file:

```bash
poetry run pytest tests/integration/users/test_users.py -v
```

View coverage report:

```bash
poetry run task coverage
# Then open htmlcov/index.html in your browser
```

## 🎨 Code Quality

### Linting

```bash
poetry run task lint
```

### Formatting

```bash
poetry run task format
```
