class OrganizationData:
    def __init__(self):
        self.org_id = None
        self.full_name = ""
        self.short_name = ""
        self.address = ""
        self.phones = []
        self.contacts = []

    def validate(self):
        return all([self.full_name, self.short_name, self.address, self.phones, self.contacts])