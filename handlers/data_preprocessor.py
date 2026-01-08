from handlers.data import OrganizationData
from handlers.person_form import Person

class DataPreprocessor:
        
    @staticmethod
    def transform_record_to_objects(record):
        result_map = {}

        for row in record:
            org_id, full_name, short_name, address, email, org_phone, contact_id, name, position, contact_email, contact_phones = row

            if org_id not in result_map:
                new_org = OrganizationData()
                new_org.org_id = org_id
                new_org.full_name = full_name
                new_org.short_name = short_name
                new_org.address = address
                new_org.email = email
                result_map[org_id] = new_org

            existing_org = result_map[org_id]
            if org_phone not in existing_org.phones:
                result_map[org_id].phones.append(org_phone)
            
            person = next((contact for contact in existing_org.contacts if contact.contact_id == contact_id), None)

            if person is None:
                person = Person()
                person.contact_id = contact_id
                person.name = name
                person.post = position
                person.email = contact_email
                person.phones.append(contact_phones)
                result_map[org_id].contacts.append(person)
            else:
                if contact_phones not in person.phones:
                    person.phones.append(contact_phones)

        return list(result_map.values())