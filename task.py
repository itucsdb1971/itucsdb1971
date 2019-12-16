class Task:
    def __init__(self, name, status, description=None, list_id=None, deadline=None, assign=None, location=None):
        self.name = name
        self.description = description
        self.list_id = list_id
        self.deadline = deadline
        self.status = status
        self.assign = assign
        self.location = location
