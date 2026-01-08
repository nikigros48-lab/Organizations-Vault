from dataclasses import dataclass, field
from handlers.person_data import Person
from typing import List

@dataclass
class OrganizationData:
    org_id: int = None
    full_name: str = ''
    short_name: str = ''
    address: str = ''
    email: str = ''
    phones: List[str] = field(default_factory=list)
    contacts: List[Person] = field(default_factory=list)

    def validate(self):
        return all([self.full_name, self.short_name, self.address, self.email, self.phones, self.contacts])
