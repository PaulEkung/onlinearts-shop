# Online Arts Shopping Platform
## Setup/Installationn 
1. Clone the repository and set up the application

    - Prerequisites
      - Install Git.
      - Install Python 3.10+ and pip.
      - Install MySQL Server and MySQL Workbench.

    - Clone repo
      - git clone <https://github.com/PaulEkung/onlinearts-shop>
      - cd <artisan>

    - Backend: create virtual environment and install requirements
      - python -m venv venv
      - Windows: venv\Scripts\activate
      - macOS/Linux: source venv/bin/activate
      - pip install --upgrade pip
      - pip install -r requirements.txt

    - MySQL: create database and user (use MySQL Workbench or run these SQL commands)
      - CREATE DATABASE artisan_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
      - CREATE USER 'artisan_user'@'localhost' IDENTIFIED BY 'your_password';
      - GRANT ALL PRIVILEGES ON artisan_db.* TO 'artisan_user'@'localhost';
      - FLUSH PRIVILEGES;

    - Configure application environment
      - Copy example env file: cp .env.example .env (Windows: copy .env.example .env)
      - Edit .env and set DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD and any other required keys.

    - Apply database schema / migrations
      - If Django:
         - python manage.py makemigrations
         - python manage.py migrate
      - If Flask with Flask-Migrate:
         - flask db upgrade
      - If the repo includes an init script:
         - python scripts/init_db.py

    - Seed data (if provided)
      - Check for a seed or fixtures script and run it, e.g. python manage.py loaddata initial_data.json or python scripts/seed.py

    - Frontend (if applicable)
      - cd frontend
      - npm install
      - npm run build   # or npm start for dev

    - Run the application
      - Backend dev server examples:
         - Django: python manage.py runserver
         - Flask: flask run
      - Visit http://localhost:8000 or the port indicated in .env

    - Common troubleshooting
      - Check .env values and DB connectivity (mysql -u artisan_user -p -h 127.0.0.1 artisan_db).
      - Inspect logs or terminal output for missing packages or migration errors.
      - Ensure MySQL server is running and user privileges are correct.

    - Useful commands summary
      - git pull
      - source venv/bin/activate (or venv\Scripts\activate)
      - pip install -r requirements.txt
      - python manage.py migrate / flask db upgrade
      - python manage.py runserver / flask run

