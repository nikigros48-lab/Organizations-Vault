import sqlite3

class DataBase:
    location = "database/db.db"

    @classmethod
    def insert_data(cls, data):
        conn = sqlite3.connect(cls.location)
        cursor = conn.cursor()
        try:
            with conn:
                cursor.execute(
                    """
                    INSERT INTO organizations (full_name, short_name, address)
                    VALUES (:full_name, :short_name, :address)
                    """,
                    {
                        'full_name': data['full_name'],
                        'short_name': data['short_name'],
                        'address': data['address']
                    }
                )

                org_id = cursor.lastrowid

                for phone in data["phones"]:
                    cursor.execute(
                        """
                        INSERT INTO organization_phones (org_id, phone_number)
                        VALUES (:org_id, :phone_number)
                        """,
                        {'org_id': org_id, 'phone_number': phone}
                    )
                
                for contact in data['contacts']:
                    cursor.execute(
                        """
                        INSERT INTO contacts (name, position, org_id)
                        VALUES (:name, :position, :org_id)
                        """,
                        {'name': contact['name'], 'position': contact['post'], 'org_id': org_id}
                    )
                    
                    contact_id = cursor.lastrowid
                    
                    for phone in contact['phones']:
                        cursor.execute(
                            """
                            INSERT INTO contact_phones (contact_id, phone_number)
                            VALUES (:contact_id, :phone_number)
                            """,
                            {'contact_id': contact_id, 'phone_number': phone}
                        )
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
            raise

    @classmethod
    def update_data(cls, updated_data):
        conn = sqlite3.connect(cls.location)
        cursor = conn.cursor()
        try:
            with conn:
                cls._update_organization(cursor, updated_data)
                cls._update_organization_phones(cursor, updated_data)
                cls._update_contacts(cursor, updated_data)
                cls._update_contact_phones(cursor, updated_data)
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
            raise

    @classmethod
    def _update_organization(cls, cursor, data):
        cursor.execute(
            """
            UPDATE organizations SET full_name=:full_name, short_name=:short_name, address=:address
            WHERE org_id=:org_id
            """,
            {
                'org_id': data['org_id'],
                'full_name': data['full_name'],
                'short_name': data['short_name'],
                'address': data['address']
            }
        )

    @classmethod
    def _update_organization_phones(cls, cursor, data):
        cursor.execute("DELETE FROM organization_phones WHERE org_id=:org_id", {'org_id': data['org_id']})
        for phone in data['phones']:
            cursor.execute(
                """
                INSERT INTO organization_phones (org_id, phone_number)
                VALUES (:org_id, :phone_number)
                """,
                {'org_id': data['org_id'], 'phone_number': phone}
            )

    @classmethod
    def _update_contacts(cls, cursor, data):
        cursor.execute("DELETE FROM contacts WHERE org_id=:org_id", {'org_id': data['org_id']})
        for contact in data['contacts']:
            cursor.execute(
                """
                INSERT INTO contacts (name, position, org_id)
                VALUES (:name, :position, :org_id)
                """,
                {'name': contact['name'], 'position': contact['post'], 'org_id': data['org_id']}
            )

    @classmethod
    def _update_contact_phones(cls, cursor, data):
        cursor.execute("DELETE FROM contact_phones WHERE contact_id IN (SELECT contact_id FROM contacts WHERE org_id=:org_id)", {'org_id': data['org_id']})
        for contact in data['contacts']:
            for phone in contact['phones']:
                cursor.execute(
                    """
                    INSERT INTO contact_phones (contact_id, phone_number)
                    VALUES ((SELECT contact_id FROM contacts WHERE name=:name AND org_id=:org_id), :phone_number)
                    """,
                    {'name': contact['name'], 'org_id': data['org_id'], 'phone_number': phone}
                )

    @classmethod
    def search_data(cls, search_text):
        conn = sqlite3.connect(cls.location)
        cursor = conn.cursor()

        sql_query = f"""
        SELECT o.org_id, o.full_name, o.short_name, o.address, op.phone_number AS org_phone,
            c.contact_id, c.name, c.position, cp.phone_number AS contact_phone
        FROM organizations o
        LEFT JOIN organization_phones op ON o.org_id = op.org_id
        LEFT JOIN contacts c ON o.org_id = c.org_id
        LEFT JOIN contact_phones cp ON c.contact_id = cp.contact_id
        WHERE o.address LIKE ? OR o.full_name LIKE ? OR o.short_name LIKE ? OR c.name LIKE ?
        """

        cursor.execute(sql_query, (f'%{search_text}%', f'%{search_text}%', f'%{search_text}%', f'%{search_text}%'))

        results = cursor.fetchall()
        conn.close()
        return results