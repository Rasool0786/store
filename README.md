````markdown
# Online Store REST API (Django REST Framework)

A robust, fully decoupled e-commerce and inventory management backend API built with Python, Django, and Django REST Framework (DRF). This project implements scalable API endpoints, clean database relationships, and modern backend practices suitable for integration with any frontend framework (React, Vue, mobile apps, etc.).

## 🚀 Features

- **Decoupled RESTful API:** Built entirely using Django REST Framework (DRF) with clean URL routing and serialization.
- **Comprehensive Product Management:** Endpoints for products, categories, subcategories, brands, and specifications.
- **Advanced Inventory Control:** Track product variations (colors, sizes), prices, and real-time stock levels.
- **Cart & Order Processing:** Dynamic endpoints to handle shopping carts, order creation, and status tracking.
- **Clean Database Relations:** Optimized models with proper foreign keys and many-to-many relationships tailored for performance.

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **API Framework:** Django REST Framework (DRF)
- **Database:** SQLite (Development) / PostgreSQL compatible
- **Version Control:** Git & GitHub with optimized `.gitignore`

## 📂 Project Structure

```text
├── core/                  # Main project settings & URL routing
├── products/              # API apps handling products, brands, and categories
├── orders/                # API apps handling cart logic and order processing
├── accounts/              # User management and authentication APIs
├── manage.py              # Django management script
├── .gitignore             # Git exclusion file
└── requirements.txt       # Project dependencies
```
````

## ⚙️ Installation & Setup

1. **Clone the repository:**

```bash
   git clone [https://github.com/Rasool0786/store.git](https://github.com/Rasool0786/store.git)
   cd store

```

2. **Create and activate a virtual environment:**

```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

```

3. **Install dependencies:**

```bash
   pip install -r requirements.txt

```

4. **Apply database migrations:**

```bash
   python manage.py migrate

```

5. **Create a superuser for the admin panel:**

```bash
   python manage.py createsuperuser

```

6. **Run the development server:**

```bash
   python manage.py runserver

```

The API will be available at `http://127.0.0.1:8000/`.

## 🔒 Future Roadmap / Upcoming Enhancements

- [ ] Integrating JWT Authentication (Simple JWT) for secure API endpoints.
- [ ] Connecting third-party Payment Gateways via API.
- [ ] Implementing Redis and Celery for asynchronous background tasks.
- [ ] Documenting endpoints using Swagger/ReDoc (drf-spectacular).
