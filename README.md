# practice deploying flask, postgres on heroku
Copied db from ETL-project

## Live site:
http://transit-systems.herokuapp.com/

## Tech Stack: 
**Back-end**: Python, Flask, SQLAlchemy, SQL (PostgreSQL)<br/>
**Front-end**: HTML, CSS, Bootstrap

### Steps:
1. Created the db and tables in PostgreSQL (see also [ELT-project](https://github.com/ellemonke/ETL-project)).
2. Created a Heroku app with a Postgres add-on.
3. Pushed my local db (with data) to the remote Heroku db.
`heroku pg:push mylocaldb DATABASE_URL --app transit-systems`
4. Defined Python functions to query the remote db using SQLAlchemy reflection (app.py).
5. Create a front-end website with Flask and Bootstrap (app.py).