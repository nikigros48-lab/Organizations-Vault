import os
import sqlite3
from handlers.data import OrganizationData

class DataBase:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.dirname(script_dir)
    location = os.path.join(root_dir, 'database', 'db.db')

    @classmethod
    def create_database(cls):
        conn = sqlite3.connect(cls.location)
        cursor = conn.cursor()

        cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS organizations(
            org_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            short_name TEXT NOT NULL,
            address TEXT NOT NULL,
            email TEXT NOT NULl
        );
        ''')

        cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS organization_phones(
            phone_id INTEGER PRIMARY KEY,
            org_id INTEGER NOT NULL,
            phone_number TEXT NOT NULL,
            FOREIGN KEY (org_id) REFERENCES organizations(org_id)
        );
        ''')

        cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS contacts(
            contact_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY (org_id) REFERENCES organizations(org_id)
        );
        ''')

        cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS contact_phones(
            phone_id INTEGER PRIMARY KEY,
            contact_id INTEGER NOT NULL,
            phone_number TEXT NOT NULL,
            FOREIGN KEY (contact_id) REFERENCES contacts(contact_id)
        );
        ''')

        conn.commit()
        conn.close()

    @classmethod
    def insert_data(cls, data:OrganizationData):
        conn = sqlite3.connect(cls.location)
        cursor = conn.cursor()
        try:
            with conn:
                cursor.execute(
                    """
                    INSERT INTO organizations (full_name, short_name, address, email)
                    VALUES (:full_name, :short_name, :address, :email)
                    """,
                    {
                        'full_name': data.full_name,
                        'short_name': data.short_name,
                        'address': data.address,
                        'email': data.email
                    }
                )

                org_id = cursor.lastrowid

                for phone in data.phones:
                    cursor.execute(
                        """
                        INSERT INTO organization_phones (org_id, phone_number)
                        VALUES (:org_id, :phone_number)
                        """,
                        {'org_id': org_id, 'phone_number': phone}
                    )
                
                for contact in data.contacts:
                    cursor.execute(
                        """
                        INSERT INTO contacts (name, position, org_id, email)
                        VALUES (:name, :position, :org_id, :email)
                        """,
                        {'name': contact.name, 'position': contact.post, 'org_id': org_id, 'email': contact.email}
                    )
                    
                    contact_id = cursor.lastrowid
                    
                    for phone in contact.phones:
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
    def update_data(cls, updated_data:OrganizationData):
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
    def _update_organization(cls, cursor, data:OrganizationData):
        cursor.execute(
            """
            UPDATE organizations SET full_name=:full_name, short_name=:short_name, address=:address, email=:email
            WHERE org_id=:org_id
            """,
            {
                'org_id': data.org_id,
                'full_name': data.full_name,
                'short_name': data.short_name,
                'address': data.address,
                'email': data.email
            }
        )

    @classmethod
    def _update_organization_phones(cls, cursor, data:OrganizationData):
        cursor.execute("DELETE FROM organization_phones WHERE org_id=:org_id", {'org_id': data.org_id})
        for phone in data.phones:
            cursor.execute(
                """
                INSERT INTO organization_phones (org_id, phone_number)
                VALUES (:org_id, :phone_number)
                """,
                {'org_id': data.org_id, 'phone_number': phone}
            )

    @classmethod
    def _update_contacts(cls, cursor, data:OrganizationData):
        cursor.execute("DELETE FROM contacts WHERE org_id=:org_id", {'org_id': data.org_id})
        for contact in data.contacts:
            cursor.execute(
                """
                INSERT INTO contacts (name, position, org_id, email)
                VALUES (:name, :position, :org_id, :email)
                """,
                {'name': contact.name, 'position': contact.post, 'org_id': data.org_id, 'email': data.email}
            )

    @classmethod
    def _update_contact_phones(cls, cursor, data:OrganizationData):
        cursor.execute("DELETE FROM contact_phones WHERE contact_id IN (SELECT contact_id FROM contacts WHERE org_id=:org_id)", {'org_id': data.org_id})
        for contact in data.contacts:
            for phone in contact.phones:
                cursor.execute(
                    """
                    INSERT INTO contact_phones (contact_id, phone_number)
                    VALUES ((SELECT contact_id FROM contacts WHERE name=:name AND org_id=:org_id), :phone_number)
                    """,
                    {'name': contact.name, 'org_id': data.org_id, 'phone_number': phone}
                )

    @classmethod
    def search_data(cls, search_text):
        conn = sqlite3.connect(cls.location)
        cursor = conn.cursor()

        sql_query = f"""
        SELECT o.org_id, o.full_name, o.short_name, o.address, o.email, op.phone_number AS org_phone,
            c.contact_id, c.name, c.position, c.email, cp.phone_number AS contact_phone
        FROM organizations o
        LEFT JOIN organization_phones op ON o.org_id = op.org_id
        LEFT JOIN contacts c ON o.org_id = c.org_id
        LEFT JOIN contact_phones cp ON c.contact_id = cp.contact_id
        WHERE o.address LIKE ? OR o.full_name LIKE ? OR o.short_name LIKE ? OR c.name LIKE ?
        """

        cursor.execute(sql_query, ((f'%{search_text}%',)*4))

        results = cursor.fetchall()
        conn.close()
        return results