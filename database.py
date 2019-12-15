import psycopg2 as dbapi2

from task import Task
from list import List
from user import User


class Database:
    def __init__(self, db_url):
        self.db_url = db_url

    def add_task(self, task):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO tasks (name, description) VALUES (%s, %s) RETURNING id"
            cursor.execute(query, (task.name, task.description))
            connection.commit()
            task_key, = cursor.fetchone()
        return task_key

    def update_task(self, task_key, task):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "UPDATE tasks SET name = %s, description = %s WHERE (id = %s)"
            cursor.execute(query, (task.name, task.description, task_key))
            connection.commit()

    def delete_task(self, task_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM tasks WHERE (id = %s)"
            cursor.execute(query, (task_key,))
            connection.commit()

    def get_task(self, task_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT name, description FROM tasks WHERE (id = %s)"
            cursor.execute(query, (task_key,))
            try:
                name, description = cursor.fetchone()
            except TypeError:
                return None
        task_ = Task(name, description=description)
        return task_

    def get_tasks(self):
        tasks = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT id, name, description FROM tasks ORDER BY id"
            cursor.execute(query)
            for task_key, name, description in cursor:
                tasks.append((task_key, Task(name, description)))
        print(tasks)
        return tasks

    def add_list(self, list):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO lists (name, description) VALUES (%s, %s) RETURNING id"
            cursor.execute(query, (list.name, list.description))
            connection.commit()
            list_key, = cursor.fetchone()
        return list_key

    def update_list(self, list_key, list):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "UPDATE lists SET name = %s, description = %s WHERE (id = %s)"
            cursor.execute(query, (list.name, list.description, list_key))
            connection.commit()

    def delete_list(self, list_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM lists WHERE (id = %s)"
            cursor.execute(query, (list_key,))
            connection.commit()

    def get_list(self, list_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT name, description FROM lists WHERE (id = %s)"
            cursor.execute(query, (list_key,))
            try:
                name, description = cursor.fetchone()
            except TypeError:
                return None
        list_ = List(name, description=description)
        return list_

    def get_lists(self):
        lists = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT id, name, description FROM lists ORDER BY id"
            cursor.execute(query)
            for list_key, name, description in cursor:
                lists.append((list_key, List(name, description)))
        print(lists)
        return lists

    def add_task_with_list(self, task):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO tasks (name, description, list_id) VALUES (%s, %s, %s) RETURNING id"
            cursor.execute(query, (task.name, task.description, task.list_id))
            connection.commit()
            task_key, = cursor.fetchone()
        return task_key

    def get_tasks_with_list(self, list_key):
        tasks = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT id, name, description FROM tasks WHERE list_id = %s ORDER BY id"
            cursor.execute(query, (list_key,))
            for task_key, name, description in cursor:
                tasks.append((task_key, Task(name, description)))
        print(tasks)
        return tasks

    def is_username_taken(self, username):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT name FROM users WHERE (name = %s)"
            cursor.execute(query, (username,))
            try:
                name = cursor.fetchone()
                if name is None:
                    return False
            except TypeError:
                return True
        return True

    def get_user(self, username):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT name, password FROM users WHERE (name = %s)"
            cursor.execute(query, (username,))
            try:
                name, password = cursor.fetchone()
            except TypeError:
                return None
        user_ = User(name, password)
        return user_

    def add_user(self, username, password):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO users (name, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            connection.commit()

    def delete_user(self, username):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM users WHERE (name = %s)"
            cursor.execute(query, (username,))
            connection.commit()

