class Person:
    def __init__(self):
        self.name = None
        self.post = None
        self.phones = []

    def validation(self):
        return all([self.name, self.post, self.phones])