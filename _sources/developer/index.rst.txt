Developer Guide
===============

Database Design
---------------

There are 3 main tables (users, tasks, lists) and 2 additional tables
(list_user_relations, task_user_relations) that holds the relations between
main tables.


E/R Diagram:

   .. figure:: images/dbdiagram.png
      :scale: 100%
      :alt: E/R Diagram

      E/R Diagram

Optional fields showed as "NULL" in E/R Diagram. Others are necessary.


A task in "tasks" table contains information for a task such as description,
status etc.

Creating a list is way of organizing multiple tasks. Lists have a name and
description (optional) which are going to be held in "lists" table.

A task inside "tasks" table has a foreign key to "lists" table in its
"list_id" column, if it is in a list.

Information about which users can see specific tasks or lists is in
"list_user_relations" and "task_user_relations" tables. These tables only
has 2 foreign key fields and an id.

Code Structure
--------------

All initial statements for a creating a database like this is inside
"dbinit.py" file and these statements gets executed every time server runs.
Mentioned initial statements are below:

   .. code-block:: python

      INIT_STATEMENTS = [
        "CREATE TABLE IF NOT EXISTS lists ("
        "id SERIAL PRIMARY KEY,"
        "name VARCHAR(80) NOT NULL,"
        "description VARCHAR(80)"
        ")",
        "CREATE TABLE IF NOT EXISTS tasks ("
        "id SERIAL PRIMARY KEY,"
        "name VARCHAR(80) NOT NULL,"
        "description VARCHAR(80),"
        "deadline DATE,"
        "status INTEGER NOT NULL,"
        "assign VARCHAR(80),"
        "location VARCHAR(80),"
        "list_id INTEGER REFERENCES lists(id) ON DELETE CASCADE"
        ")",
        "CREATE TABLE IF NOT EXISTS users("
        "name VARCHAR(80) PRIMARY KEY,"
        "password TEXT NOT NULL"
        ")",
        "CREATE TABLE IF NOT EXISTS task_user_relations ("
        "id SERIAL PRIMARY KEY,"
        "task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,"
        "username VARCHAR(80) NOT NULL REFERENCES users(name) ON DELETE CASCADE"
        ")",
        "CREATE TABLE IF NOT EXISTS list_user_relations ("
        "id SERIAL PRIMARY KEY,"
        "list_id INTEGER NOT NULL REFERENCES lists(id) ON DELETE CASCADE,"
        "username VARCHAR(80) NOT NULL REFERENCES users(name) ON DELETE CASCADE"
        ")",
       ]

There 2 different configs in "settings.py" file and if flask environment is
"production", "ProductionConfig" gets activated which gets "DATABASE_URL"
from environment variables from Heroku for ElephantSQL otherwise
"DevelopmentConfig" gets activated which sets "DATABASE_URL" to
"postgres://postgres:docker@localhost:5432/postgres" for development on
local with Docker PostgreSQL.

All database related functions are inside "database.py".

---------------------------------------
All Parts Implemented by Emre HORSANALI
---------------------------------------