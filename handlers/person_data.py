class Person:
    def __init__(self):
        self.contact_id = None
        self.name = ""
        self.post = ""
        self.email = ""
        self.phones = []

    def validation(self):
        return all([self.name, self.post, self.email, self.phones])