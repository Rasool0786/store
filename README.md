# Online Store Backend (Django)

An e-commerce and inventory management backend system built with Python and Django. This project implements clean database relationships, scalable architectural patterns, and robust logic tailored for modern web applications.

## 🚀 Features

- **Comprehensive Product Catalog:** Supports categories, subcategories, brands, and detailed product specifications.
- **Advanced Inventory & Stock Management:** Tracks stock levels, product variations (colors, sizes), and pricing history.
- **Dynamic Cart & Order System:** Multi-step checkout process with complete order tracking and status management.
- **User Authentication & Profiles:** Personalized dashboards for customers to track orders and manage addresses.
- **Robust Database Architecture:** Optimized queries using modern ORM practices to avoid N+1 problems.

## 🛠️ Tech Stack

- **Backend:** Python, Django (MVC Pattern)
- **Database:** SQLite (Development) / PostgreSQL compatible
- **Styling/Frontend:** Integrated Django Templates with Bootstrap/CSS

## 📂 Project Structure

```text
├── core/                  # Project configuration (settings, urls, wsgi)
├── products/              # Product, Category, and Brand management
├── orders/                # Cart, Checkout, and Order processing
├── accounts/              # Custom User model and authentication
├── templates/             # Global HTML templates
├── manage.py
└── requirements.txt
```

## ⚙️ Installation & Setup

```text
1.Clone the repository:
git clone [https://github.com/Rasool0786/store.git](https://github.com/Rasool0786/store.git)
cd store

2.Create and activate a virtual environment:
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3.Install dependencies:
pip install -r requirements.txt

4.Apply database migrations:
python manage.py migrate

5.Create a superuser for the admin panel:
python manage.py createsuperuser

6.Run the development server:
python manage.py runserver

Open http://127.0.0.1:8000/ in your browser.
```

## 🔒Future Roadmap / Upcoming Enhancements

- Transitioning completely to Django REST Framework (DRF) for a decoupled API architecture.

- Integrating third-party Payment Gateways.

- Implementing Redis and Celery for asynchronous task queues (e.g., sending order emails).

- Adding advanced search and filtering functionality using Elasticsearch.
