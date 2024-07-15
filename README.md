# Tiretutor backend task

This is a backend challenge for Tiretutor.

# Installation

## Prerequisites:

Please have these installed
- python3.12
- pipenv
- git

## Steps:

1. Clone the repository:

    ```bash
    git clone git@github.com:halicki/tiretutor-backend-task.git
    ```

2. Install dependencies:

    ```bash
    cd tiretutor-backend-task
    pipenv install
    ```

3. Migrate the database:

    ```bash
    pipenv run python manage.py migrate
    ```

4. Create a superuser:

    ```bash
    pipenv run python manage.py createsuperuser
    ```

5. Run the server:
    ```bash
    pipenv run python manage.py runserver
    ```
