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
            query = "INSERT INTO tasks (name, description, deadline) VALUES (%s, %s, %s) RETURNING id"
            cursor.execute(query, (task.name, task.description, task.deadline))
            connection.commit()
            task_key, = cursor.fetchone()
        return task_key

    def update_task(self, task_key, task):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "UPDATE tasks SET name = %s, description = %s, deadline = %s WHERE (id = %s)"
            cursor.execute(query, (task.name, task.description, task.deadline, task_key))
            connection.commit()

    def delete_task(self, task_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM tasks WHERE (id = %s)"
            cursor.execute(query, (task_key,))
            connection.commit()

    def get_task(self, task_key, username):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT a.name, a.description, a.deadline FROM tasks a, task_user_relations b " \
                    "WHERE (b.username = %s and b.task_id = a.id and a.id = %s)"
            cursor.execute(query, (username, task_key))
            try:
                name, description, deadline = cursor.fetchone()
            except TypeError:
                return None
        task_ = Task(name, description=description, deadline=deadline)
        return task_

    def get_tasks(self, username):
        tasks = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT a.id, a.name, a.description, a.deadline FROM tasks a, task_user_relations b " \
                    "WHERE (b.username = %s and b.task_id = a.id) ORDER BY a.id"
            cursor.execute(query, (username,))
            for task_key, name, description, deadline in cursor:
                tasks.append((task_key, Task(name, description=description, deadline=deadline)))
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

    def get_list(self, list_key, username):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT a.name, a.description FROM lists a, list_user_relations b " \
                    "WHERE (b.username = %s and b.list_id = a.id and a.id = %s)"
            cursor.execute(query, (username, list_key))
            try:
                name, description = cursor.fetchone()
            except TypeError:
                return None
        list_ = List(name, description=description)
        return list_

    def get_lists(self, username):
        lists = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT a.id, a.name, a.description FROM lists a, list_user_relations b " \
                    "WHERE (b.username = %s and b.list_id = a.id) ORDER BY a.id"
            cursor.execute(query, (username,))
            for list_key, name, description in cursor:
                lists.append((list_key, List(name, description)))
        return lists

    def add_task_with_list(self, task):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO tasks (name, description, deadline, list_id) VALUES (%s, %s, %s, %s) RETURNING id"
            cursor.execute(query, (task.name, task.description, task.deadline, task.list_id))
            connection.commit()
            task_key, = cursor.fetchone()
        return task_key

    def get_tasks_with_list(self, list_key):
        tasks = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT id, name, description, deadline FROM tasks WHERE list_id = %s ORDER BY id"
            cursor.execute(query, (list_key,))
            for task_key, name, description, deadline in cursor:
                tasks.append((task_key, Task(name, description=description, deadline=deadline)))
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

    def add_task_user_relation(self, task_key, username):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO task_user_relations (task_id, username) VALUES (%s, %s)"
            cursor.execute(query, (task_key, username))
            connection.commit()

    def add_list_user_relation(self, list_key, username):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO list_user_relations (list_id, username) VALUES (%s, %s)"
            cursor.execute(query, (list_key, username))
            connection.commit()

    def get_task_share(self, task_key):
        usernames = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT username FROM task_user_relations WHERE (task_id = %s)"
            cursor.execute(query, (task_key,))
            for username in cursor:
                usernames.append(username[0])
        return usernames

    def delete_task_user_relation(self, task_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM task_user_relations WHERE (task_id = %s)"
            cursor.execute(query, (task_key,))
            connection.commit()

    def is_exist_task_user_relation(self, task_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT task_id, username FROM task_user_relations WHERE (task_id = %s)"
            cursor.execute(query, (task_key,))
            try:
                task_key, username = cursor.fetchone()
            except TypeError:
                return False
        return True

    def count_task_user_relation(self, task_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT COUNT(task_id) FROM task_user_relations WHERE (task_id = %s)"
            cursor.execute(query, (task_key,))
            try:
                count = cursor.fetchone()
            except TypeError:
                return 0
        return count

    def task_add_list(self, list_key, task_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "UPDATE tasks SET list_id = %s WHERE (id = %s)"
            cursor.execute(query, (list_key, task_key))
            connection.commit()

    def task_remove_list(self, task_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "UPDATE tasks SET list_id = NULL WHERE (id = %s)"
            cursor.execute(query, (task_key,))
            connection.commit()
