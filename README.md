# Github tool
A simple github tool
The app can be accessed [HERE](https://cdvx-github-tool.herokuapp.com/)

## Product Description
- A user logs into the application with their github
- User can then view a list of their repositories

## Development set up

#### Set up 

- Check that python 3, pip, virtualenv and postgres are installed

- Clone repo and cd into it
    ```
    git clone https://github.com/cdvx/github_tool.git
    ```
- Create virtual env
    ```
    python3 -m venv venv
    ```
- Activate virtual env
    ```
    . venv/bin/activate
    ```
- Install dependencies
    ```
    pip install -r requirements.txt
    ```
- Create Application environment variables and save them in .env  sample file
    ```
   SECRET = 'Secret Key'
   FLASK_ENV = 'development'
   PORT = 5000
   DATABASE_URL_PROD = "postgresql://{DB_HOST}/{DB_NAME}?user={DB_USER}&password={DB_PASSWORD}"
   DATABASE_URL_DEV = "postgresql://{DB_HOST}/{DB_NAME}?user={DB_USER}&password={DB_PASSWORD}"
   DATABASE_URL_TEST = "postgresql://{DB_HOST}/{DB_NAME}?user={DB_USER}&password={DB_PASSWORD}"

    ```
- Running migrations
    - create a migration file
        ```
        python manage.py db migrate
        ```
    - Apply Migrations
        ```
        python manage.py db upgrade
        ```

- Run application.
    ```
    python manage.py runserver
    ```

        ```
 

## Built with
- Python version  3
- Flask
- Postgres

## Author
Cedric Lusiba
