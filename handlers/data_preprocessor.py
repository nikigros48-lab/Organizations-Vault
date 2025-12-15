from handlers.data import OrganizationData
from handlers.person_form import Person

class DataPreprocessor:
    @staticmethod
    def prepare_data(data_obj):
        return {
            "org_id" : data_obj.org_id,
            "full_name" : data_obj.full_name,
            "short_name" : data_obj.short_name,
            "address" : data_obj.address,
            "phones" : data_obj.phones,
            "contacts" : [
                {"name" : person.name, "post" : person.post, "phones" : person.phones}
                for person in data_obj.contacts
            ]
        }
    
    @staticmethod
    def transform_record_to_objects(record):
        result_map = {}

        for row in record:
            org_id, full_name, short_name, address, org_phone, contact_id, name, position, contact_phones = row

            if org_id not in result_map:
                new_org = OrganizationData()
                new_org.org_id = org_id
                new_org.full_name = full_name
                new_org.short_name = short_name
                new_org.address = address
                new_org.phones.append(org_phone)
                result_map[org_id] = new_org
            else:
                existing_org = result_map[org_id]
                if org_phone not in existing_org.phones:
                    existing_org.phones.append(org_phone)

            if contact_id is not None:
                new_person = Person()
                new_person.name = name
                new_person.post = position
                new_person.phones.append(contact_phones)

                result_map[org_id].contacts.append(new_person)

        return list(result_map.values())