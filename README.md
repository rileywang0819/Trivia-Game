# Trivia Game Application


TODO: API doc

TODO: Project doc


This project is a trivia app which can

- Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
- Delete questions.
- Add questions and require that they include question and answer text.
- Search for questions based on a text query string.
- Play the quiz game, randomizing either all questions or within a specific category.


## Tech Stack

- Flask
- Flask-CORS
- Flask-SQLAlchemy
- Unittest


## Getting Started

### Pre-requisites

Developers using this project should already have `Python3`, `pip` and `node` installed on their local machines.

### Backend

#### **Start your virtual environment**

It is recommended that working within a virtual environment whenever running Python projects.This keeps dependencies for each project separated and organaized. If you want to set up a virtual environment for your platform, from the `./backend` folder run

```bash
pip install virtualenv

python -m virtualenv env

# Mac/Linux users
source ven/bin/activate
# Windows users
source ven/Scripts/activate
```

You can find more details in [Python Docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### **Install dependencies**

To install dependencies, navigating to the `./backend` folder and running

```bash
# All required packages are included in the requirements file. 
pip install -r requirements.txt
```

#### **Run the project**

- **Step 0: Start or stop the PostgreSQL server**

> click [here](https://tableplus.com/blog/2018/10/how-to-start-stop-restart-postgresql-server.html) for reference.

- **Step 1: Create and populate the database**

1. Verify the db username<br>
Verify that the database user in `./backend/trivia.psql`, `./backend/models.py` and `./backend/test_flaskr.py` files must be correct (`postgres` default).

2. Create the database<br>
In terminal, navigate to the `./backend` directory and run

```bash
# Connect to the PostgreSQL
psql -U postgres

#View all databases
\l

# Create the database
\i setup.sql

# Exit the PostgreSQL prompt
\q
```

3. Create tables<br>
Once databases are created, create table and apply constrains,

```bash
# Mac users
psql -f trivia.psql -U postgres -d trivia

# Linux users
su - postgres bash -c "psql trivia < ./backend/trivia.psql"
```

*You can even drop the database and repopulate it, if needed, using the commands above.*

- **Step 2: Start the backend server**

Start (backend) Flask server by running the command below from the `/backend` directory.

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in `flaskr` folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the Flask documentation.

The application will run on http://127.0.0.1:5000/ by default and is set as a proxy in the frontend configuration. 

The current version of the application does not require authentication or API keys.


### Frontend

The `./fronten`d directory contains a complete React frontend to consume the data from the Flask server. You can view the [README](https://github.com/rileywang0819/Trivia-Game/blob/master/frontend/README.md) within `./frontend` for more details.

### Testing

If any exercise needs testing, navigate to the `./backend` folder and run the following command,

```bash
python test_flaskr.py
```

## API Reference

Details in this [page](https://github.com/rileywang0819/Trivia-Game/blob/master/backend/README.md).
