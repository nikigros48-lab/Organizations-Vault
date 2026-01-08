from dataclasses import dataclass, field
from typing import List

@dataclass
class Person:
    contact_id: int = None
    name: str = ''
    post: str = ''
    email: str = ''
    phones: List[str] = field(default_factory=list)

    def validation(self):
        return all([self.name, self.post, self.email, self.phones])
