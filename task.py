class Task:
    def __init__(self, name, description=None, list_id=None, deadline=None):
        self.name = name
        self.description = description
        self.list_id = list_id
        self.deadline = deadline
