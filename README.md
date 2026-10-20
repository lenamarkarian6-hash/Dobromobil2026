# Добромобиль

Сайт помощи приютам для животных. Django + HTML/CSS/JS.

## Запуск

    python -m venv venv

Windows:

    venv\Scripts\activate

Linux/Mac:

    source venv/bin/activate

Затем:

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py create_roles
    python manage.py createsuperuser
    python manage.py runserver

Откройте http://127.0.0.1:8000/
