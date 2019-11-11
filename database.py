import psycopg2 as dbapi2

from task import Task


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
