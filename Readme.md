# Django Real Estate Platform

A fully functional real estate web application built with Django and Tailwind CSS. Users can browse properties, leave reviews with ratings, and book listings. Admin users can manage listings through the admin panel or directly from the site.

---

## 🌐 Live Demo

You can test the project online:  
[Render.com demo](https://your-render-link.onrender.com)

---

## 🚀 Local Setup

Follow these steps to run the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/NikaL25/real-estate_django.git
cd real-estate

2. Create a virtual environment
python -m venv venv
```

## Activate it:

Windows:

```
venv\Scripts\activate
```

Linux / macOS:

```
source venv/bin/activate
```

## 3. Install dependencies
```pip install -r requirements.txt
```

If you don’t have a requirements.txt, create it after installing packages:

```
pip freeze > requirements.txt
```

## 4. Apply migrations
```python manage.py makemigrations
python manage.py migrate
```

## 5. Create a superuser (for admin access)
```
python manage.py createsuperuser
```
Follow the prompts to enter username, email, and password.

## 6. Run the development server
```
python manage.py runserver
```

Visit:

http://127.0.0.1:8000/

⚡ Features
For all users:

Browse all property listings

View detailed property pages

For registered users:

Register and log in

Leave reviews and ratings (1–10 stars)

Book properties

View personal bookings and reviews

For admin users:

Edit or delete listings directly on the site

Access full Django admin panel

🛠 Technologies

Python 3.10+

Django 5.2

Tailwind CSS for UI styling

SQLite (default, can switch to Postgres or MySQL)