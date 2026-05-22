# Nova Store — Django E-Commerce Platform

A complete, modern e-commerce web application built with **Django 5.2** and **Vanilla JavaScript**.

## Features
- Product listings with category filters & search
- Product detail pages with related products
- Shopping cart (add, remove, update quantity) — guest + logged-in users
- Checkout with shipping form and payment method selection
- Order confirmation & order history
- User registration & login/logout
- Django Admin panel for managing everything

## Requirements
- Python 3.10+ (tested on 3.14)
- pip

## Setup

```bash
# 1. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows PowerShell
# OR: venv\Scripts\activate.bat   # if above fails

# 2. Install dependencies
pip install Django==5.2 python-dotenv==1.0.1

# 3. Setup .env
copy .env.example .env

# 4. Run migrations
python manage.py makemigrations store
python manage.py makemigrations accounts
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Load sample products (RECOMMENDED)
python manage.py load_sample_data

# 7. Start server
python manage.py runserver
```

Open: **http://127.0.0.1:8000/**
Admin: **http://127.0.0.1:8000/admin/**

## Tech Stack
Django 5.2 · SQLite · HTML5 · CSS3 · Vanilla JS · Font Awesome
