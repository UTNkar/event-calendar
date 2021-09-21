# event-calendar

- Description Todo

  ## Getting Started
1. Install Python 3, at least version 3.6 or up.
2. Install the following python packages:
   - python3-venv
   - python3-dev
   - build-essentials
   - libpq-dev
3. Clone the repository.
4. Run `source ./source_me.sh` to create a virtual environment.
4. Run `pip install --upgrade pip` to make sure that pip is running the latest version
5. Run `pip install -r dev-requirements.txt`
6. Use `cd src` to enter the website directory.
7. Run `./manage.py migrate` to initialize the database.
8. Run `./manage.py createsuperuser` to create an admin user.
9. Open another terminal and run `./manage.py tailwind start`

During development, you can run a test web server using `./manage.py runserver`.

**IMPORTANT!** When running any command in moore, you must be in the virtual environment (a.k.a. `source source_me.sh`)
