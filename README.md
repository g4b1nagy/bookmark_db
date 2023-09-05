# Bookmark DB

Put your bookmark collection to good use


## How do I set this up for development?

    git clone git@github.com:g4b1nagy/bookmark_db.git
    cd bookmark_db/
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ./bin/create_database_and_user.sh bookmark_db bookmark_db bookmark_db
    ./manage.py migrate
    DJANGO_SUPERUSER_PASSWORD="admin" ./manage.py createsuperuser --noinput --username admin --email admin@bookmark.db
    ./manage.py import utils/test_files/
    ./manage.py runserver
    go to http://localhost:8000/admin/


## How do I run the tests?

    ./manage.py test
